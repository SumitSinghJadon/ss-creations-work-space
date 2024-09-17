from django.http import JsonResponse
from django.views import View
from QMS_db.models import ObDetail,ObMaster
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
import json
from django.db import connections
from QMS_db.models import OrderMt 
from django.middleware.csrf import get_token
import json
from datetime import datetime 
from IS_Nexus.functions.shortcuts import get_next_number

class ExcelDataShowView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
    def prepare_sql(self, request):
        """ Create query to fetch data from ERP with Filter (Selected by user)  """
        filter_string = 'WHERE t1.ourref is not NULL'
        buyer_filter = request.GET.get('buyer_filter')
        style_filter = request.GET.get('style_filter')
        
        if buyer_filter:
            filter_string += f" and t2.buyer = '{buyer_filter}'"
          
        if style_filter:
            filter_string += f" and t1.styleno = '{style_filter}'"

        if buyer_filter and style_filter:
            # print(buyer_filter,style_filter)
            
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
                    select t2.styleno from ExpoHead t1
                    join expolotdet t2 on t1.ourref = t2.ourref
                    where t1.buyer = '{buyer_filter}'
            '''
            cursor.execute(sql)
            data = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            # print(data)
            return data
        else:
            response_data = {} 
            response_data['csrf_token'] = get_token(request)  
            return response_data
        
    @csrf_exempt
    def get(self, request):
        try:
            data = self.prepare_sql(request)
            context = {
                'data': data,
            }
            return JsonResponse(context)
        except Exception as e:
            print(f"Error in Excel Data Get view: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    
        

    # @csrf_exempt
    # def post(self, request, *args, **kwargs):
    #     try:
    #         data = json.loads(request.body)
    #         print("Received data:", data)  

    #         headers = data.get('header')
    #         colValue = data.get('sendData')
    #         buyer = data.get('buyer')
    #         buyer_name = data.get('buyer_name')
    #         style = data.get('style')
    #         color = data.get('color')
    #         obDate = data.get('obDate')
    #         reCutting = float(data.get('reCutting', 0))
    #         kazButton = float(data.get('kazButton', 0))
    #         other = float(data.get('other', 0))

    #         total_line_sam = 0.0
    #         total_line_sum = len(colValue)

    #         ob_no = None  # Initialize ob_no here
    #         if buyer and style:
    #             ob_no = get_next_number(ObMaster, "OB")
    #             Mt = ObMaster.objects.create(
    #                 buyer_code=buyer,
    #                 buyer_name=buyer_name,
    #                 style=style,
    #                 line_sum=total_line_sum,
    #                 ob_no=ob_no,
    #                 ob_date=obDate,
    #                 re_cutting=reCutting,
    #                 kaz_button=kazButton,
    #                 other=other,
    #                 color=color
    #             )

    #             for col in colValue:
    #                 data_dict = dict(zip(headers, col))
    #                 sam = float(data_dict.get('SAM', 0.0))
    #                 total_line_sam += sam


    #                 instance = ObDetail.objects.create(
    #                     ob_mt=Mt,
    #                     ob_no=ob_no,
    #                     parts=data_dict.get('Parts'),
    #                     operation=data_dict.get('Operation'),
    #                     type_of_machine=data_dict.get('Type of Machine'),
    #                     attachments=data_dict.get('Attachments'),
    #                     sam=sam,
    #                     theoretical_manpower=data_dict.get('Theoretical Manpower'),
    #                     planned_work_station=data_dict.get('Planned Work Station'),
    #                     target_100_pcs=data_dict.get('Target @ 100% PCs/Hr'),
    #                     target_60_pcs=data_dict.get('Target @ 60% PCs/Hr'),
    #                 )

    #             total_sam = float(total_line_sam) + reCutting + kazButton + other
    #             Mt.total_sam = total_sam
    #             Mt.line_sam = total_line_sam
    #             Mt.save()

    #             data = {
    #                 'ob_no': ob_no
    #             }
    #             return JsonResponse(data)

    #         else:
    #             return JsonResponse({"error": "Missing buyer or style information"}, status=400)

    #     except json.JSONDecodeError as e:
    #         print(f'JSON Decode Error: {e}')
    #         return JsonResponse({"error": "Invalid JSON format"}, status=400)

    #     except KeyError as e:
    #         print(f'KeyError: {e}')
    #         return JsonResponse({"error": f"Missing required field: {str(e)}"}, status=400)

    #     except ValueError as e:
    #         print(f'ValueError: {e}')
    #         return JsonResponse({"error": f"Invalid value: {str(e)}"}, status=400)

    #     except Exception as e:
    #         print(f'Error: {e}')
    #         return JsonResponse({"error": str(e)}, status=500)


    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("Received data:", data)  

            headers = data.get('header')
            colValue = data.get('sendData')[1:]
            buyer = data.get('buyer')
            buyer_name = data.get('buyer_name')
            style = data.get('style')
            color = data.get('color')
            obDate = data.get('obDate')
            reCutting = float(data.get('reCutting', 0))
            kazButton = float(data.get('kazButton', 0))
            other = float(data.get('other', 0))

            total_line_sam = 0.0
            total_line_sum = len(colValue)

            ob_no = None
            if buyer and style:
                ob_no = get_next_number(ObMaster, "OB")
                Mt = ObMaster.objects.create(
                    buyer_code=buyer,
                    buyer_name=buyer_name,
                    style=style,
                    line_sum=total_line_sum,
                    ob_no=ob_no,
                    ob_date=obDate,
                    re_cutting=reCutting,
                    kaz_button=kazButton,
                    other=other,
                    color=color
                )

                for col in colValue:
                    data_dict = dict(zip(headers, col))
                    sam = float(data_dict.get('SAM', 0.0))  
                    total_line_sam += sam

                    instance = ObDetail.objects.create(
                        # ob_mt=Mt,
                        # ob_no=ob_no,
                        # parts=data_dict.get('Parts'),
                        # operation=data_dict.get('Operation'),
                        # type_of_machine=data_dict.get('Type of Machine'),
                        # attachments=data_dict.get('Attachments'),
                        # sam=sam,
                        # theoretical_manpower=data_dict.get('Theoretical Manpower'),
                        # planned_work_station=data_dict.get('Planned Work Station'),
                        # target_100_pcs=data_dict.get('Target @ 100% PCs/Hr'),
                        # target_60_pcs=data_dict.get('Target @ 60% PCs/Hr'),
                        ob_mt=Mt,
                        ob_no=ob_no,
                        parts=data_dict.get('SECTION'),
                        operation=data_dict.get('OPERATION NAME'),
                        type_of_machine=data_dict.get('TYPE OF M/Cs'),
                        attachments=data_dict.get('ATTACHMENT'),
                        sam=sam,
                        theoretical_manpower=data_dict.get('THEO. OPTRS'),
                        planned_work_station=data_dict.get('THEO. BAL. OPTRS'),
                        target_100_pcs=data_dict.get('TGT @100%'),
                        target_60_pcs=data_dict.get('TGT @60%'),
                        seam_length = data_dict.get('Seam Length'),
                        remark = data_dict.get('Remarks')
                    )

                total_sam = round(float(total_line_sam) + reCutting + kazButton + other,2)
                Mt.total_sam = total_sam
                Mt.line_sam = round(total_line_sam,2)
                Mt.save()

                data = {
                    'ob_no': ob_no
                }
                return JsonResponse(data)

            else:
                return JsonResponse({"error": "Missing buyer or style information"}, status=400)

        except json.JSONDecodeError as e:
            print(f'JSON Decode Error: {e}')
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except KeyError as e:
            print(f'KeyError: {e}')
            return JsonResponse({"error": f"Missing required field: {str(e)}"}, status=400)

        except ValueError as e:
            print(f'ValueError: {e}')
            return JsonResponse({"error": f"Invalid value: {str(e)}"}, status=400)

        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({"error": str(e)}, status=500)

        

class ObDetailsView(View):
    def get_ob_data(self,request):
        buyer = request.GET.get('buyer')
        style = request.GET.get('styleno')
        color = request.GET.get('color')
        if buyer and style  :
            ob_mt=ObMaster.objects.get(buyer_code=buyer,style=style)
            print(ob_mt)
        elif buyer and style and color :
            ob_mt=ObMaster.objects.get(buyer_code=buyer,style=style,color=color)
            print(ob_mt)
        else :
            ob_data={'message':"Ob not Upload"}
        ob_data = ObDetail.objects.filter(ob_mt=ob_mt.id).values('operation','id').distinct('operation')
        return list(ob_data)
    
    def get_all_ob_master(self,request):
        all_ob_mt_data = ObMaster.objects.all().values()
        return list(all_ob_mt_data)
        
    def get(self,request):
        ob_data = self.get_ob_data(request)
        ob_mt_data = self.get_all_ob_master(request)
        context ={
            'ob_data':ob_data,
            'ob_mt_data':ob_mt_data
        }
        return JsonResponse(context,safe=False)
    
    
class ObDetailsShowView(View):  
    @csrf_exempt
    def get(self,request):
        id = int(request.GET.get('id'))
        print(type(id))
        print("id",id)
       
        ob_data=ObDetail.objects.filter(ob_mt=id).values()
        print("ob_data",ob_data)
        ob_data_list = list(ob_data) 
        context ={
            'ob_show_data':ob_data_list
        }
        return JsonResponse(context,safe=False)
    

    
    
    
        
class ObMasterView(View):
    def get_all_ob_master(self,request):
        all_ob_mt_data = ObMaster.objects.all().values().order_by('-id')
        return list(all_ob_mt_data)
        
    def get(self,request):
        ob_mt_data = self.get_all_ob_master(request)
        context ={
            'ob_mt_data':ob_mt_data
        }
        return JsonResponse(context,safe=False)
    