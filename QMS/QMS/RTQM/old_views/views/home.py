from django.shortcuts import render, redirect
from django.views import View
from QMS_db.models import OrderDt
from QMS_db.models import OrderMt  
from django.db import connections
from django.views.decorators.csrf import csrf_exempt  # Add By Sudhir
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token # Add By Sudhir
from django.http import JsonResponse
from IntelliSync_db.models import MenuMaster


@method_decorator(csrf_exempt, name='dispatch')
class Home(View):
    def get(self, request):
        menu = list(MenuMaster.objects.filter(module_id=7).values())
        context = {
            'menu': list(menu), 
        }
        return JsonResponse(context, safe=False)
        