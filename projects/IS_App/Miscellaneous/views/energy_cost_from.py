from django.shortcuts import render
from django.views import View
from IntelliSync_db.models.location_master import LocationMaster
from IntelliSync_db.models.common_master import FirstLevelMaster
from IntelliSync_db.models.common_master import CommonMaster
from django.db.models import F , IntegerField
from IntelliSync_db.models import CommonMaster
from django.db.models.functions import Cast
from datetime import datetime , date
from django.db.models import Q
from django.db import connections
from django.http import JsonResponse

class EnergyCostView(View):
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

        flag = request.GET.get('flag')
        head = request.GET.get('head')

        if flag == 'get_head_by_unit':
            sql_query = f"""
                    select * from is_intellisync_db.dbo.common_master 
                    where master_type_id ='41' and is_active = '1';
                """
            with connections["default"].cursor() as cursor:
                cursor.execute(sql_query)
                head = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return JsonResponse(head, safe=False)
        
        elif flag == 'get_sub_head_by_head':
            sql_query = f"""
                   select * from is_intellisync_db.dbo.first_level_master 
                   where common_master_type_id ='41' and common_master_id ='{head}';    
                """
            with connections["default"].cursor() as cursor:
                cursor.execute(sql_query)
                sub_head = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            return JsonResponse(sub_head, safe=False)
        
        units = LocationMaster.objects.values('name')
        dayno = date(year, month, 1)
        month_list=CommonMaster.objects.filter(master_type__code='CT-19').annotate(
            m_name = F("name"),
            m_num = F("value"),
            index=Cast('value', output_field=IntegerField())
        ).values('m_name', 'm_num').order_by('index')
        
        context = {
            'unit':units,
            'month_list' : month_list,
            'year_list' : range(2021,year+1),
            'month' :month,
            'year' :year,
            'dayno':dayno,
        }
        return render(request, 'energy_cost_form.html',context)