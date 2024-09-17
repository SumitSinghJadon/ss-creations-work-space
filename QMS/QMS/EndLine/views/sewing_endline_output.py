from django.views import View
from django.http import HttpResponse, JsonResponse
from QMS_db.models import SewingLineInputMt, SewingLineInputDt



class SewingEndLineOutputView(View):
    def get(self, request):
        pass 

    def post(self, request):
        planning = request.POST.get('planning')
         
