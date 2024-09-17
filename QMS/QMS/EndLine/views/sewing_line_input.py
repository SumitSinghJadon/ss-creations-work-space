from django.views import View
from django.http import HttpResponse, JsonResponse
from QMS_db.models import SewingLineInputMt, SewingLineInputDt, SewingPlanning
import json



class SewingLineInputPlanView(View):
    def get(self, request):
        line = request.GET.get(id=line)
        planning_list = SewingPlanning.objects.filter(line = line, is_closed=False, is_active=True).values(
            'buyer_name'
        )
        data = list(planning_list)
        return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})


class SewingLineInputView(View):
    def get(self, request):
        def get_size_wise_qty():
            pass 

    def post(self, request):
        pass 
            
