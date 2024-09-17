from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster
from django.db import connections
from django.contrib import messages
from Miscellaneous.models import OtApproval
from datetime import datetime , timedelta

class CuttingReportView(View):
    def get(self,request):
        unit_code = request.GET.get('unit_code')
        dayno = request.GET.get('dayno')

        unit_list = LocationMaster.objects.filter(is_active=True)
        data_list =[]
        data_list_total =[]
        data_list_revenue =[]
        pnl =0


        if unit_code:
            date_parts = datetime.strptime(dayno, "%Y-%m-%d")
            month = date_parts.month
            year = date_parts.year

            unit_code_erp = LocationMaster.objects.get(payroll_code =unit_code)
            
            unit_code_erp = unit_code_erp.erp_code
            # print(unit_code_erp)
            cursor = connections['default'].cursor()
            sql = f"""  EXEC GET_CUTTING_DATA_ERP '{dayno}','{unit_code_erp}','cutting' """
            cursor.execute(sql)
            
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            # print(data_list)
            cursor.close()

            cursor = connections['default'].cursor()
            sql = f"""  EXEC GET_DAILY_MANP_LIST_DEPT_COST '{month}','{year}','{unit_code}',22,'one_day_total_cost','{dayno}' """
            # print(sql)
            cursor.execute(sql)
            data_list_total =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()] or 0
            cursor.close()

            cursor = connections['default'].cursor()
            sql = f"""  EXEC GET_CUTTING_DATA_ERP '{dayno}','{unit_code_erp}','cutting_total' """
            cursor.execute(sql)
            data_list_revenue =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()] or 0
            cursor.close()
            print(data_list_revenue)
            if data_list_total[0]['today_cost'] and data_list_revenue[0]['total_revenue']:
                pnl = float(data_list_revenue[0]['total_revenue']) - float(data_list_total[0]['today_cost'])
        
        # print(data_list)
        context = {
            'unit_list' :unit_list,
            'unit_code' :unit_code,
            'dayno' :dayno,
            'data_list' : data_list,
            'data_list_total' : data_list_total,
            'data_list_revenue' : data_list_revenue,
            'pnl' : pnl

        }
        return render(request,'cutting_trans.html',context)
    

