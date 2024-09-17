from django.http import JsonResponse
from django.views import View
from QMS_db.models import RtqmMt, RtqmCounter
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

class RtqmAPI(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        buyer = request.GET.get('buyer')
        styleno = request.GET.get('style')  # Ensure this matches the query parameter name
        color = request.GET.get('color')
        ourref = request.GET.get('ourref')

        # Check if all required parameters are provided
        if not all([buyer, styleno, color, ourref]):
            logger.error('Missing required parameters: buyer=%s, style=%s, color=%s, ourref=%s',
                         buyer, styleno, color, ourref)
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        try:
            response_data = self.counter_rtqm_pdrr(buyer, styleno, color, ourref)
            return JsonResponse(response_data, status=200)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    def counter_rtqm_pdrr(self, buyer, styleno, color, ourref):
        try:
            rtqm_mt = RtqmMt.objects.get(buyer_code=buyer, style=styleno, color=color, ourref=ourref)
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
