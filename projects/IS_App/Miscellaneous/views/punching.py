from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster ,CommonMaster
from IS_Nexus.database import get_unit_list,get_month_punch_list
from django.db import connections
from datetime import datetime , timedelta
from django.db.models.functions import Cast
from django.db.models import F , IntegerField

class Punchdata(View):
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

        curr_year = int(datetime.today().strftime('%Y'))
        curr_month = int(datetime.today().strftime('%m'))
        # print(curr_month , curr_year , month , year)

        month_list=CommonMaster.objects.filter(master_type__code='CT-19').annotate(
            m_name = F("name"),
            m_num = F("value"),
            index=Cast('value', output_field=IntegerField())
        ).values('m_name', 'm_num').order_by('index')

        context = {
            'month_list' : month_list,
            'year_list' : range(2021,curr_year+1),
            'numday' : range(1,32),
            'unit_list' : unit_list,
            'punch_list' : get_month_punch_list(str(month),str(year),unit_code)
        }
        return render(request,'punching.html',context)
    
    def post(self,request):
        pass
