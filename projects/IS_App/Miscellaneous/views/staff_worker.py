from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster , CommonMaster
from IS_Nexus.database import get_unit_list,get_staff_worker_today_list
from django.db import connections
from datetime import datetime , timedelta
from django.db.models.functions import Cast
from django.db.models import F , IntegerField

class Staff_worker(View):
    def get(self,request):
        unit_code = request.GET.get('unit_code')
        if request.GET.get('month') :
            month = int(request.GET.get('month'))
        else :
            month = int(datetime.today().strftime('%m'))
        if request.GET.get('year') :
            year = int(request.GET.get('year'))
        else :
            year = int(datetime.today().strftime('%Y'))
        unit_list = LocationMaster.objects.filter(is_active=True)
        today_date = datetime.today().strftime('%d-%m-%Y')

        curr_year = int(datetime.today().strftime('%Y'))
        curr_month = int(datetime.today().strftime('%m'))
        # print(curr_month , curr_year , month , year)

        month_list=CommonMaster.objects.filter(master_type__code='CT-19').annotate(
            m_name = F("name"),
            m_num = F("value"),
            index=Cast('value', output_field=IntegerField())
        ).values('m_name', 'm_num').order_by('index')
        
        yesterday = datetime.now() - timedelta(days=1)
        prev_date = yesterday.strftime('%d-%m-%Y')

        # print(prev_date,today_date,str(month2),str(year),unit_code)

        context = {
            'month_list' : month_list,
            'year_list' : range(2021,curr_year+1),
            'numday' : range(1,32),
            'unit_list' : unit_list,
            'today_date' : today_date,
            'prev_date' : prev_date,
            'unit_code' : unit_code,
            'staff_worker_list' : get_staff_worker_today_list(prev_date,today_date,str(month),str(year),'1')
        }
        return render(request,'staff_worker.html',context)
