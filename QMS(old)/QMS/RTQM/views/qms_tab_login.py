from django.views import View
from django.http import JsonResponse
from IntelliSync_db.models import FirstLevelMaster 
from django.views.decorators.csrf import csrf_exempt  
from django.utils.decorators import method_decorator
import json


class QmsTabLogin(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    def get_line_data(self,request):
        first_level =FirstLevelMaster.objects.filter(master_type__code='CT-37').values()
        return list(first_level)
    
    @csrf_exempt
    def get(self, request):
        try:
            first_level_master = self.get_line_data(request)
            context = {
                'line_master_data': list(first_level_master),
            }
            return JsonResponse(context)

        except Exception as e:
            print(f"Error in QmsPlaning2 view: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
