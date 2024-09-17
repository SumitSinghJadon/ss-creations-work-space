from django.http import JsonResponse
from django.views import View
from QMS_db.models import RtqmMt, RtqmCounter
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator
import logging
from datetime import date
logger = logging.getLogger(__name__)

class RtqmAPI(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        id = request.GET.get("id")
        
        if not id:
            logger.error('Missing required parameter: id')
            return JsonResponse({'error': 'Missing required parameter: id'}, status=400)

        try:
            total_counter_data = self.counter_rtqm_pdrr(id)
            today_counter_pdrr = self.today_counter_pdrr(id)
            context ={
                'total_counter_data':total_counter_data,
                'today_counter_pdrr':today_counter_pdrr
            }
            
            return JsonResponse(context, status=200)
        except RtqmMt.DoesNotExist:
            return JsonResponse({'error': 'RtqmMt object not found'}, status=404)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    def counter_rtqm_pdrr(self, id):
        try:
            rtqm_mt = RtqmMt.objects.get(planing__id=id)
        except RtqmMt.DoesNotExist:
            return {'error': 'RtqmMt object not found'}

        pass_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt, status='RFT').count()
        defect_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt, status='DEFECT').count()
        reject_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt, status='REJECT').count()
        rectified_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt, rectified='RECTIFIED').count()

        response_data = {
            'pass_count': pass_count,
            'defect_count': defect_count,
            'reject_count': reject_count,
            'rectified_count': rectified_count
        }

        return response_data

    def today_counter_pdrr(self,id):
        try:
            entry_date = date.today().strftime('%m/%d/%Y')
            rtqm_mt = RtqmMt.objects.get(planing__id=id)
        except RtqmMt.DoesNotExist:
            return {'error': 'RtqmMt object not found'}

        pass_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt,entry_date=entry_date, status='RFT').count()
        defect_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt,entry_date=entry_date, status='DEFECT').count()
        reject_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt,entry_date=entry_date, status='REJECT').count()
        rectified_count = RtqmCounter.objects.filter(rtqm_mt=rtqm_mt,entry_date=entry_date, rectified='RECTIFIED').count()

        response_data = {
            'today_pass_count': pass_count,
            'today_defect_count': defect_count,
            'today_reject_count': reject_count,
            'today_rectified_count': rectified_count
        }
        return response_data
        