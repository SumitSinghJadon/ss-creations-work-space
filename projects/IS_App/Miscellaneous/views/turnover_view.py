from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster
from django.db import connections
from django.contrib import messages
from Miscellaneous.models import OtApproval
from datetime import datetime , timedelta
import json

class SaleTurnoverView(View):
    def get(self,request):
        

        if request.GET.get('from_date'):
            from_date = request.GET.get('from_date')
            from_date_filt = datetime.strptime(from_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            from_date = datetime.now().strftime("01-%m-%Y")
            from_date_filt = datetime.now().strftime("%Y-%m-01")
        if request.GET.get('to_date'):
            to_date = request.GET.get('to_date')
            to_date_filt = datetime.strptime(to_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            to_date = datetime.now().strftime("%d-%m-%Y")
            to_date_filt = datetime.now().strftime("%Y-%m-%d")
        
        unit_list = LocationMaster.objects.filter(is_active=True)
        data_list =[]
        unit_code = ''
        unit_code_erp = ''



        # print(unit_code_erp)
        cursor = connections['default'].cursor()
        
        sql1 = f"""  EXEC GET_SALE_TURNOVER '{from_date_filt}', '{to_date_filt}',  """
        
        if request.GET.get('unit_code'):
            unit_code = request.GET.get('unit_code')
            unit_code_erp = LocationMaster.objects.get(payroll_code =unit_code)
            unit_code_erp = unit_code_erp.erp_code
            sql2 = f"""  '{unit_code_erp}',  """
        else:
            sql2 = f"""  NULL,  """
        if request.GET.get('unit_code') == 'turnover_details':
            sql3 = f"""  'details'  """
        else:
            sql3 = f"""  'details'  """
            
        sql = sql1 + sql2 + sql3    
        cursor.execute(sql)
        print(sql)
        data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        json_result = json.dumps(data_list)
        # print(data_list)
        cursor.close()
        
        # print(data_list)
        context = {
            'unit_code_erp' :unit_code_erp,
            'unit_list' :unit_list,
            'unit_code' :unit_code,
            'from_date' :from_date,
            'to_date' :to_date,
            'from_date_filt' :from_date_filt,
            'to_date_filt' :to_date_filt,
            'data_list' : data_list,
        }
        return render(request,'turnover_view.html',context)
    

