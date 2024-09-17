import datetime
from datetime import  timedelta

import logging
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views import View
from QMS_db.models  import RtqmMt,RtqmDt,RtqmCounter,RtqmDefectDT
import json
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
from IntelliSync_db.models import get_next_number
from QMS_db.models.masters.defect_master import DefectMaster
from QMS_db.models.ob_master import ObDetail
from django.db import transaction

from QMS_db.models.qms_planing import QmsPlaning

logger = logging.getLogger(__name__)

class RTQMView(View):
    def get(self, request):
        context = {}
        return render(request, 'rtqm.html', context)

    def post(self, request):
        return render("RTQM_page")


class RtqmDtMtView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            # print(data)
            quantity = data.get('quantity')
            size = data.get('size')
            defect_operation = data.get('defect_operation')
            status = data.get('status')
            rtqm_mt_data = data.get('rtqm_mt_data')
            rtqm_counter_id = data.get('rtqm_counter_id','')
            current_time = datetime.datetime.now().strftime('%H:%M') 
            entry_date = datetime.datetime.today().strftime('%m/%d/%Y')

            existing_rtqm_mt = RtqmMt.objects.filter(
                    planing__id=rtqm_mt_data['id'],
                ).first()

            if existing_rtqm_mt:
                existing_rtqm_mt.total_quantity += int(quantity)
                existing_rtqm_mt.save()
                rtqm_mt = existing_rtqm_mt
            else:
                rtqm_no = get_next_number('RTQM')
                planing = QmsPlaning.objects.get(id=rtqm_mt_data['id'])
                rtqm_mt = RtqmMt.objects.create(
                    planing=planing,
                    rtqm_no=rtqm_no,
                )
            existing_rtqm_dt = RtqmDt.objects.filter(
                                rtqm_mt=rtqm_mt,
                                size=size
                            ).first()

            if existing_rtqm_dt:
                if status == 'RFT':
                    existing_rtqm_dt.total_rtf += quantity
                elif status == 'REJECT':
                    existing_rtqm_dt.total_reject += quantity
                elif status == 'DEFECT':
                    existing_rtqm_dt.total_defect += quantity
                elif status == 'RECTIFIED':
                    existing_rtqm_dt.total_rectified += quantity

                existing_rtqm_dt.total_quantity += quantity
                existing_rtqm_dt.save()
                rtqm_dt = existing_rtqm_dt
            else:
                rtqm_dt_no = get_next_number('RTQM-Dt')
                rtqm_dt = RtqmDt.objects.create(
                    rtqm_mt=rtqm_mt,
                    rtqm_dt_no=rtqm_dt_no,
                    rtqm_no=rtqm_mt.rtqm_no,
                    size=size,
                    total_quantity=quantity,
                )

                if status == 'RFT':
                    rtqm_dt.total_rtf += quantity
                elif status == 'REJECT':
                    rtqm_dt.total_reject += quantity
                elif status == 'DEFECT':
                    rtqm_dt.total_defect += quantity
                elif status == 'RECTIFIED':
                    rtqm_dt.total_rectified += quantity

                rtqm_dt.save()
            if rtqm_counter_id:
                existing_rtqm_counter =RtqmCounter.objects.get(id=rtqm_counter_id)
                if existing_rtqm_counter:
                    prv_df_count = existing_rtqm_counter.defect_counter
                    existing_rtqm_counter.defect_counter = 1 + prv_df_count
                    # print("Conter data hai bhai",existing_rtqm_counter)
                    
                    existing_rtqm_counter.save()
                    rtqm_counter = existing_rtqm_counter
            else:
                
                
                rtqm_counter = RtqmCounter.objects.create(
                rtqm_no=rtqm_mt.rtqm_no,
                rtqm_dt=rtqm_dt,
                rtqm_mt=rtqm_mt,
                rtqm_dt_no=rtqm_dt.rtqm_dt_no,
                status=status,
                rectified=data.get('rectified'),
                entry_date=entry_date,
                entry_time=current_time,
                )
            
                            
            defect_dt_list = []
            for operation in defect_operation[0]:  
                ob_detail_id = operation['id']
                
                for defect in operation['defects']:
                    defect_id = defect['id']
                    dfId = defect['id']  
                    
                    sf_x = None
                    sf_y = None
                    for front_coord in operation['frontCoordinates']:
                        if front_coord['dfId'] == defect_id:
                            sf_x = front_coord['x']
                            sf_y = front_coord['y']
                            break  
                    
                    sb_x = None
                    sb_y = None
                    for back_coord in operation['backCoordinates']:
                        if back_coord['dfId'] == defect_id:
                            sb_x = back_coord['x']
                            sb_y = back_coord['y']
                            break  
                        
                    data = {
                        'ob_detail_id': ob_detail_id,
                        'defect': defect_id,
                        'dfId': dfId,
                        'sf_x': sf_x,
                        'sf_y': sf_y,
                        'sb_x': sb_x,
                        'sb_y': sb_y
                    }
                    
                    defect_dt_list.append(data)
            for defect_dt in defect_dt_list:
                ob_instance = ObDetail.objects.get(id=defect_dt['ob_detail_id']) 
                defect_instance = DefectMaster.objects.get(id=defect_dt['defect'])  
                
                rtqm_defect_dt = RtqmDefectDT.objects.create(
                    rtqm_dt_no=rtqm_dt.rtqm_dt_no,
                    rtqm_no=rtqm_mt.rtqm_no,
                    rtqm_mt=rtqm_mt,
                    rtqm_dt=rtqm_dt,
                    rtqm_counter=rtqm_counter,
                    ob_detail=ob_instance,
                    ob_name = ob_instance.operation,
                    defect_name = defect_instance.name,
                    defect=defect_instance,
                    sf_x=defect_dt['sf_x'],
                    sf_y=defect_dt['sf_y'],
                    sb_x=defect_dt['sb_x'],
                    sb_y=defect_dt['sb_y'],
                    entry_date=entry_date,
                    entry_time=current_time,
                    size = size,
                )
            return JsonResponse({'message': 'Data processed successfully'}, status=200)

        except KeyError as e:
            logger.error(f"KeyError in RtqmMtView: {str(e)}")
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)

        except Exception as e:
            logger.error(f"Error type: {type(e)}, Error message: {str(e)}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    def rtqm_defect_filter(self,request):
        rtqm_dt_df = list(RtqmDt.objects.filter('total_defect').values())

    def get(self,request):
        rtqm_dt_defect = self.rtqm_defect_filter(request)
        context ={
            'rtqm_dt_defect_' :rtqm_dt_defect,
        }
        return JsonResponse (context,safe=False)



class RtqmMtDtPassView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity')
            pass_data = data.get('pass_data')
            status = data.get('status')
            rtqm_mt_data = data.get('rtqm_mt_data')
            current_time = datetime.datetime.now().strftime('%H:%M') 
            current_date = datetime.datetime.now().strftime('%m/%d/%Y') 
            # print(quantity) 

            with transaction.atomic():
                existing_rtqm_mt = RtqmMt.objects.filter(
                    planing__id=rtqm_mt_data['id'],
                ).first()

                if existing_rtqm_mt:
                    existing_rtqm_mt.total_quantity += int(quantity)
                    existing_rtqm_mt.save()
                    rtqm_mt = existing_rtqm_mt
                else:
                    rtqm_no = get_next_number('RTQM')
                    planing = QmsPlaning.objects.get(id=rtqm_mt_data['id'])
                    rtqm_mt = RtqmMt.objects.create(
                        planing=planing,
                        rtqm_no=rtqm_no,
                        total_quantity = int(quantity)
                    )

                for item in pass_data:
                    size = item['size']
                    item_quantity = item['quantity']
                    entry_time =item['entry_time']
                    entry_date = item['entry_date']

                    existing_rtqm_dt = RtqmDt.objects.filter(
                        rtqm_mt=rtqm_mt,
                        size=size
                    ).first()

                    if existing_rtqm_dt:
                        if status == 'RFT':
                            existing_rtqm_dt.total_rtf += item_quantity
                        existing_rtqm_dt.total_quantity += item_quantity
                        existing_rtqm_dt.save()
                        rtqm_dt = existing_rtqm_dt
                        # print('item_quantity',item_quantity)
                        
                    else:
                        rtqm_dt_no = get_next_number('RTQM-Dt')
                        rtqm_dt = RtqmDt.objects.create(
                            rtqm_mt=rtqm_mt,
                            rtqm_dt_no=rtqm_dt_no,
                            rtqm_no=rtqm_mt.rtqm_no,
                            size=size,
                            total_quantity=item_quantity
                        )
                        if status == 'RFT':
                            rtqm_dt.total_rtf = item_quantity
                        rtqm_dt.save()
                    rtqm_counter = RtqmCounter.objects.create(
                            rtqm_no=rtqm_mt.rtqm_no,
                            rtqm_dt=rtqm_dt,
                            rtqm_mt=rtqm_mt,
                            rtqm_dt_no=rtqm_dt.rtqm_dt_no,
                            status=status,
                            rectified=None,
                            entry_date=entry_date,
                            entry_time=entry_time,
                        )

            return JsonResponse({'message': 'Data processed successfully'}, status=200)

        except KeyError as e:
            logger.error(f"KeyError in RtqmMtView: {str(e)}")
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)

        except Exception as e:
            logger.error(f"Error type: {type(e)}, Error message: {str(e)}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)




class RtqmMtDtRectifiedView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_defect_dt(self, request):
        id = request.GET.get('id')
       
        today = datetime.datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        rtqm_mt_queryset = RtqmMt.objects.filter(planing__id=id)
        # print("rtqm_mt_queryset",rtqm_mt_queryset)
        if rtqm_mt_queryset.exists():
            rtqm_counter_queryset = RtqmCounter.objects.filter(
                rtqm_mt__planing__id=id,
                status='DEFECT',
                created_at__date__in=[today, yesterday]
            ).values_list('id', flat=True) 
            
            rtqm_counter = RtqmCounter.objects.filter(
                rtqm_mt__planing__id=id,
                status='DEFECT',
                rectified =None,
                created_at__date__in=[today, yesterday]
            ).values() 
            # print("counter Data", rtqm_counter)
            
            defect_data_list = RtqmDefectDT.objects.filter(
                rtqm_counter_id__in=rtqm_counter_queryset
            ).values()  
            # print("defect Data", defect_data_list)
           
            rtqm_mt_data = list(rtqm_mt_queryset.values())
            
            return list(defect_data_list), rtqm_mt_data, list(rtqm_counter)

    def get(self, request, *args, **kwargs):
        defect_data = self.get_defect_dt(request)
        
        if defect_data is None:
            defect_data = {
                'defect_data_list': [],
                'defect_mt_data': [],
                'defect_counter': []
            }
        else:
            defect_data_list, defect_mt_data, defect_counter = defect_data
            defect_data = {
                'defect_data_list': defect_data_list,
                'defect_mt_data': defect_mt_data,
                'defect_counter': defect_counter
            }
        
        return JsonResponse(defect_data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            status = data.get('status')
            id = data.get('id')
            # id = data.get('id')
            print("data post", data)
            
            rtqm_counter = get_object_or_404(RtqmCounter, pk=id)
            print("rtqm_counter", rtqm_counter.rectified)
            
            if status == 'REJECT':
                rtqm_counter.rectified = 'REJECT'
            elif status == 'RECTIFIED':
                rtqm_counter.rectified = 'RECTIFIED'
            elif status == 'DEFECT':
                rtqm_counter.rectified = 'DEFECT'
            else:
                return JsonResponse({"error": f"Invalid status: {status}"}, status=400)
            
            rtqm_counter.save()
            return JsonResponse({"message": f"Status updated to {status}"})
        
        except RtqmCounter.DoesNotExist:
            return JsonResponse({'error': f'RtqmCounter with id {id} does not exist'}, status=404)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON format: {str(e)}'}, status=400)
        
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
        
        
        
from django.db.models import Count ,Q
        
        
class RtqmDtView(View):
    def get_size_wise_output_quantity(self,request):
        id = request.GET.get('id')
        rtqm_dt_data = RtqmDt.objects.filter(rtqm_mt__planing__id = id).values('size','total_quantity','id')
        return list(rtqm_dt_data)
    
    def get_today_size_wise_output(self,request):
        id = request.GET.get('id')
        current_date = datetime.datetime.now().strftime('%m/%d/%Y') 
        today_size_wise_qty = RtqmCounter.objects.filter(rtqm_mt__planing__id=id,entry_date =current_date).values('rtqm_dt__size').annotate(size_count=Count('rtqm_dt__size'))
        # print('Today Size wise Qty',today_size_wise_qty)
        size_output_list = []
        for item in today_size_wise_qty:
            size_count = item['size_count']
            size = item['rtqm_dt__size']
            size_output_list.append({
                'size': size,
                'size_count': size_count
            })
        return size_output_list
        
    def get_entry_rtqm(self,request):
        id = request.GET.get('id')
        if id:
            history_entries = RtqmCounter.objects.filter(
                rtqm_mt__planing__id=id
            ).values(
                'entry_date',
                'rtqm_dt__size',
                'rtqm_mt__planing__buyer_name',
                'rtqm_mt__planing__styleno',
                'status'
            ).annotate(
                count_entries=Count('entry_date', filter=Q(status='RFT'))
            )
            
            history_list = []
            for entry in history_entries:
                history_list.append({
                    'buyer_name': entry['rtqm_mt__planing__buyer_name'],
                    'size': entry['rtqm_dt__size'],
                    'styleno': entry['rtqm_mt__planing__styleno'],
                    'status': entry['status'],
                    'count_entries': entry['count_entries'],
                    'entry_date': entry['entry_date']
                })
            print ("history",history_list)
            
            return history_list
        else:
            return []
        
    def get(self,request):
        rtqm_dt_data = self.get_size_wise_output_quantity(request)
        today_size_qty = self.get_today_size_wise_output(request)
        history_list = self.get_entry_rtqm(request)
        context ={
            'rtqm_dt_data':rtqm_dt_data,
            'today_size_qty':today_size_qty,
            'history_list':history_list
        }
        return JsonResponse(context,safe=False)
        