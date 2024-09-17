from django.shortcuts import render
from django.views import View
from IntelliSync_db.models.location_master import LocationMaster
from IntelliSync_db.models.common_master import FirstLevelMaster
from IntelliSync_db.models.common_master import CommonMaster
from django.db.models import F , IntegerField
from IntelliSync_db.models import CommonMaster
from django.db.models.functions import Cast
from datetime import datetime , date


class ECFElectricityView(View):
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
        print(f" month'{month_disp}' year '{year_disp}' ")
        sub_head = FirstLevelMaster.objects.filter(common_master_type_id='41', common_master_id='172')
        head = CommonMaster.objects.filter(id='172')
        units = LocationMaster.objects.values('name')
        dayno = date(year, month, 1)
        month_list=CommonMaster.objects.filter(master_type__code='CT-19').annotate(
            m_name = F("name"),
            m_num = F("value"),
            index=Cast('value', output_field=IntegerField())
        ).values('m_name', 'm_num').order_by('index')
        print(f"head'{head}',head'{sub_head}'")
        context = {
            'sub_head':sub_head,
            'head':head,
            'unit':units,
            'month_list' : month_list,
            'year_list' : range(2021,year+1),
            'month' :month,
            'year' :year,
            'dayno':dayno
        }
        return render(request,'ECF_electricity.html',context)
        