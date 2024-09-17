from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster
from IS_Nexus.database import get_unit_list,get_dep_list,get_desg_list,get_ot_approve_excess_list,get_ot_unauth_list
from django.db import connections
from django.contrib import messages
from Miscellaneous.models import OtApproval
from datetime import datetime , timedelta

class OtApproval_unauth(View):
    def get(self,request):
        unit_code = request.GET.get('unit_code')
        dayno = request.GET.get('dayno')
        department = request.GET.get('dept')
        designation = request.GET.get('desg')
        ot_hour = request.GET.get('ot_hour')
        unit_list = LocationMaster.objects.filter(is_active=True)
        # print(dayno,department,designation,unit_code )
        context = {
            'unit_code' :unit_code,
            'dayno' :dayno,
            'ot_hour' :ot_hour,
            'ot_hour_list' : range(1,12),
            'unit_list' : unit_list,
            'dept_list' : get_dep_list(),
            'desg_list' : get_desg_list(),
            'ot_app_excess_list' : get_ot_approve_excess_list(dayno,department,designation,unit_code),
            'ot_unauth_list' : get_ot_unauth_list(dayno,department,designation,unit_code)
            # 'ot_emp_temp_list' : ot_emp_temp_list(dayno,department,designation,unit_code,user=1)
        }
        return render(request,'ot_approval_unauth.html',context)
    

