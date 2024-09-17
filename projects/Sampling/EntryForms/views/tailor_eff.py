from django.views import View
from django.shortcuts import render
from django.db.models import CharField, Value, functions, F, aggregates , IntegerField
from django.db.models.functions import Concat, Cast
from django.db import connections
from django.contrib import messages
from datetime import datetime , timedelta
from IS_Nexus.functions.shortcuts import get_next_number,pay_db
from IntelliSync_db.models import CommonMaster


class ConcatAgg(aggregates.Aggregate):
    function = 'STRING_AGG'
    template = "%(function)s(%(distinct)s%(expressions)s, '')"
    allow_distinct = True


class TailorEffView(View):
    def get(self, request):

        if request.GET.get('month') :
            month = int(request.GET.get('month'))
        else :
            month = int(datetime.today().strftime('%m'))
        if request.GET.get('year') :
            year = int(request.GET.get('year'))
        else :
            year = int(datetime.today().strftime('%Y'))

        curr_date = datetime.today().strftime('%Y-%m-%d')
        curr_year = int(datetime.today().strftime('%Y'))
        db_name = pay_db(curr_date)
        month_list=CommonMaster.objects.filter(master_type__code='CT-19').annotate(
            m_name = F("name"),
            m_num = F("value"),
            index=Cast('value', output_field=IntegerField())
        ).values('m_name', 'm_num').order_by('index')
        cursor =  connections['default'].cursor()
        if month and year:
            cursor = connections['default'].cursor()
            sql = f""" 
                EXEC GET_TAILOR_EFF '{month}','{year}','1',8,'summ','{curr_date}'
            """
            cursor.execute(sql)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()

            cursor = connections['default'].cursor()
            sql = f""" 
                EXEC GET_TAILOR_EFF '{month}','{year}','1',8,'total_summ','{curr_date}'
            """
            cursor.execute(sql)
            data_list_total =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()

        context = {
            'month' : month,
            'year' : year,
            'data_list' : data_list,
            'data_list_total' : data_list_total,
            'month_list' : month_list,
            'year_list' : range(2021,curr_year+1)
        }
        return render(request, 'tailor_eff.html', context)
    
 
        