from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster , CommonMaster
from IS_Nexus.database import get_unit_list,get_ot_emp_list,get_dep_list,get_desg_list
from django.db import connections
from django.contrib import messages
# from Miscellaneous.models import OtApproval
from datetime import datetime , timedelta , date
from django.db.models import F , IntegerField
from django.db.models.functions import Cast

class ManpowerAllocReportView(View):
    def get(self,request):
        unit_code = request.GET.get('unit_code')
        if request.GET.get('month') :
            month = int(request.GET.get('month'))
            month_disp = request.GET.get('month')
        else :
            month = int(datetime.today().strftime('%m'))
            month_disp = datetime.today().strftime('%m')
        if request.GET.get('year') :
            year = int(request.GET.get('year'))
            year_disp = request.GET.get('year')
        else :
            year = int(datetime.today().strftime('%Y'))
            year_disp = datetime.today().strftime('%Y')
            
        # dayno = datetime.today().strftime('{{year}}-{{month}}-%d')
        dayno = date(year, month, 1)
        # print(dayno)
        unit_list = LocationMaster.objects.filter(is_active=True)
        data_list = []
        if dayno and unit_code:
            cursor = connections['default'].cursor()
            sql = f""" 
                 EXEC [GET_MANPOWER_ALLOC] '{unit_code}','day_wise','{dayno}'
            """
            # print(sql)
            cursor.execute(sql)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        print(data_list)

        month_list=CommonMaster.objects.filter(master_type__code='CT-19').annotate(
            m_name = F("name"),
            m_num = F("value"),
            index=Cast('value', output_field=IntegerField())
        ).values('m_name', 'm_num').order_by('index')


        line_type_list = [{ 'name' : 'MAIN' }]
        line_name_list = [{ 'name' : 'GF' },{ 'name' : 'FF' },{ 'name' : 'SF' } ]
        context = {
            'month_list' : month_list,
            'year_list' : range(2021,year+1),
            'month' :month,
            'year' :year,
            'unit_code' :unit_code,
            'line_type_list' :line_type_list,
            'line_name_list' :line_name_list,
            'dayno' :dayno,
            'unit_list' : unit_list,
            'data_list' : data_list,
        }
        return render(request,'manpower_allocation_report.html',context)
    
