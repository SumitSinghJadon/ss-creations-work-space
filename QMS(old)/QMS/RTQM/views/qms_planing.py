
from django.shortcuts import render, redirect
from django.views import View
from django.db import connections
from django.http import JsonResponse
from QMS_db.models import OrderMt, OrderDt ,QmsPlaning
from django.views.decorators.csrf import csrf_exempt  # Add By Sudhir
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token # Add By Sudhir
# from IS_Nexus.functions.data_conversion import queryset_to_json
from django.core import serializers
import json
from datetime import datetime 
from IntelliSync_db.models import LocationMaster ,CommonMaster,FirstLevelMaster  
from IS_Nexus.database.qms import get_floor_by_unit_data,get_line_by_floor_data  
from IntelliSync_db.models import get_next_number


class QmsPlaningView(View):
    def get(self, request):
        def get_buyer_list():
            cursor = connections['erp_db'].cursor()
            sql =f'''
                SELECT distinct t2.party_code as buyer_code, t2.party_name as buyer_name
                from expohead t1
                join party t2 on t1.buyer = t2.party_code
            
            '''
            cursor.execute(sql)
            data_list = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()
            return data_list or None
        
        location_data = LocationMaster.objects.all()
        location_master_data = list(location_data.values()) 
        planing_data = self.get_planing_data(request)
        context = {
            # 'data' : get_order_data(),
            'buyer_list' : get_buyer_list(),
            'location_data':location_master_data,
            'planing_data' :planing_data,
        }
        return JsonResponse (context) 

    def get_planing_data(self, request):
        planing_data = QmsPlaning.objects.all().values(
            'id', 'buyer', 'buyer_name', 'ourref', 'styleno',
            'color', 'delvdate', 'unit', 'floor',
            'line',  
            'quantity', 'planing_no', 'planing_date',
            'is_active'
        )

        modified_data = []
        
        for entry in planing_data:
            line_id = entry['line']
            unit_id = entry['unit']
            
            try:
                line_instance = FirstLevelMaster.objects.get(id=line_id)
                unit_instance = LocationMaster.objects.get(id=unit_id)
            except FirstLevelMaster.DoesNotExist:
                line_instance = None
            
            if line_instance:
                entry['line_name'] = line_instance.name
            
            else:
                entry['line_name'] = None
            if unit_instance:
                entry['unit_name'] = unit_instance.name
            else:
                entry['unit_name'] = None
            
            modified_data.append(entry)
        
        return modified_data

    
    

    def post(self, request):
        pass 




class QmsPlaningView2(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def prepare_sql(self, request):
        """ Create query to fetch data from ERP with Filter (Selected by user)  """
        filter_string = 'WHERE t1.ourref is not NULL'
        buyer_filter = request.GET.get('buyer_filter')
        ref_filter = request.GET.get('ref_filter')
        style_filter = request.GET.get('style_filter')
        
        if buyer_filter:
            filter_string += f" and t2.buyer = '{buyer_filter}'"
        if ref_filter:
            filter_string += f" and t1.ourref = '{ref_filter}'"    
        if style_filter:
            filter_string += f" and t1.styleno = '{style_filter}'"

        if buyer_filter and ref_filter:
            cursor = connections['erp_db'].cursor()
            sql = f'''
                SELECT DISTINCT t3.delvdate, t1.ourref, t1.styleno, t1.color, t1.totalqty, 
                t2.buyer, t2.season, t2.totalpcs, t2.buyord, t2.sizetype, t4.party_name
                FROM ExpoLotDet t1
                JOIN ExpoHead t2 ON t1.ourref = t2.ourref 
                JOIN ExpoLot t3 ON t1.ourref = t3.ourref
                JOIN party t4 ON t4.party_code = t2.buyer { filter_string }
            ''' 
            cursor.execute(sql)
            data = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return data
        elif buyer_filter:
            cursor = connections['erp_db'].cursor()
            sql = f'''
                SELECT t2.ourref
                FROM ExpoHead t1
                JOIN expolotdet t2 ON t1.ourref = t2.ourref
                WHERE t1.buyer = '{buyer_filter}'
            '''
            cursor.execute(sql)
            data = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return data
        else:
            response_data = {} 
            response_data['csrf_token'] = get_token(request)  
            return response_data
        
    def get_floor_data(self, request):
        unit_id = request.GET.get('unit_id')
        common_master = get_floor_by_unit_data(unit_id)
        return common_master
    
    
    def get_line_data(self,request):
        common_id = request.GET.get('common_id')
        first_level =FirstLevelMaster.objects.filter(master_type__code='CT-37',common_master_id=common_id).values()
        return list(first_level)
    
    def get_planing_data(self,request):
        line_id = request.GET.get('line_id')
        planing_data = QmsPlaning.objects.filter(line_id=line_id).values()
        return list(planing_data)
    
    @csrf_exempt
    def get(self, request):
        try:
            data = self.prepare_sql(request)
            common_master = self.get_floor_data(request)
            first_level_master = self.get_line_data(request)
            planing_data = self.get_planing_data(request)

            context = {
                'data': data,
                'common_master_data': common_master,
                'line_master_data': list(first_level_master),
                'planing_data' : planing_data
                
            }

            return JsonResponse(context)

        except Exception as e:
            print(f"Error in QmsPlaning2 view: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)



    def post(self, request):
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            delvdate = datetime.strptime(request_data['delvdate'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            planing_date = datetime.strptime(request_data['planing_date'], "%Y-%m-%d").date()
            planing_no  = get_next_number('SewingPlan')
            qms_planing = QmsPlaning.objects.create(
                buyer=request_data['buyer'],
                buyer_name = request_data['buyer_name'],
                ourref=request_data['ourref'],
                styleno=request_data['styleno'],
                color=request_data['color'],
                delvdate=delvdate,
                unit_id=request_data['unit'],
                floor_id=request_data['floor'],
                line_id=request_data['line'],
                quantity=int(request_data['quantity']), 
                planing_date=planing_date,
                planing_no=planing_no
            )

            return JsonResponse({'message': 'QmsPlaning created successfully.'}, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'error': f'Invalid value: {e}'}, status=400)

        except Exception as e:
            print(f"Error creating QmsPlaning: {e}")  # Log the error for debugging
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    # # def post(self, request):
    #     try:
    #         request_data = json.loads(request.body.decode('utf-8'))
    #         delvdate = datetime.strptime(request_data['delvdate'], "%Y-%m-%dT%H:%M:%S.%fZ").date()  # Adjust format for delvdate
    #         planing_date = datetime.strptime(request_data['planing_date'], "%Y-%m-%d").date()  # Adjust format for planing_date
    #         print (request_data)
    #         qms_planing = QmsPlaning.objects.create(
    #             buyer=request_data['buyer'],
    #             ourref=request_data['ourref'],
    #             styleno=request_data['styleno'],
    #             color=request_data['color'],
    #             delvdate=delvdate,
    #             unit_id=request_data['unit'],
    #             floor_id=request_data['floor'],
    #             line_id=request_data['line'],
    #             quantity=int(request_data['quantity']),  # Ensure quantity is converted to integer
    #             planing_date=planing_date
    #         )

    #         return JsonResponse({'message': 'QmsPlaning created successfully.'}, status=201)

    #     except KeyError as e:
    #         return JsonResponse({'error': f'Missing required field: {e}'}, status=400)

    #     except ValueError as e:
    #         return JsonResponse({'error': f'Invalid value: {e}'}, status=400)

    #     except Exception as e:
    #         return JsonResponse({'error': str(e)}, status=500)