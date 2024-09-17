from django.views import View
from django.shortcuts import render
from django.db.models import F, aggregates , IntegerField
from django.db.models.functions import Cast
from django.db import connections
from django.contrib import messages
from datetime import datetime
from IS_Nexus.functions.shortcuts import get_next_number,pay_db
from IntelliSync_db.models import CommonMaster


class ConcatAgg(aggregates.Aggregate):
    function = 'STRING_AGG'
    template = "%(function)s(%(distinct)s%(expressions)s, '')"
    allow_distinct = True


class SamplingCostView(View):
    def get(self, request):

        if request.GET.get('month') :
            month = int(request.GET.get('month'))
        else :
            month = int(datetime.today().strftime('%m'))
        if request.GET.get('year') :
            year = int(request.GET.get('year'))
        else :
            year = int(datetime.today().strftime('%Y'))

        if request.GET.get('dept') :
            dept = int(request.GET.get('dept'))
        else :
            # select CONDIDTION from SystemParameters where ParameterName ='SAMP_DEPT'
            cursor = connections['is_app'].cursor()
            sql = f"""  select CONDIDTION from SystemParameters where ParameterName ='SAMP_DEPT' """
            cursor.execute(sql)
            dept_arr =  cursor.fetchone()
            cursor.close()
            dept = dept_arr[0]

        curr_date = datetime.today().strftime('%Y-%m-%d')
        curr_year = int(datetime.today().strftime('%Y'))
        db_name = pay_db(curr_date)
        
        cursor = connections['default'].cursor()
        sql = f""" 
            select dep_code,dep_name from {db_name}.dbo.tbdep where dep_name like 'SAMP%' order by dep_name asc
        """
        cursor.execute(sql)
        data_list_dept =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        cursor.close()
            
            
        month_list=CommonMaster.objects.filter(master_type__code='CT-19').annotate(
            m_name = F("name"),
            m_num = F("value"),
            index=Cast('value', output_field=IntegerField())
        ).values('m_name', 'm_num').order_by('index')
        cursor =  connections['default'].cursor()
        if month and year:
            cursor = connections['is_app'].cursor()
            sql1 = f"""  EXEC GET_DAILY_MANP_LIST_DEPT_COST '{month}','{year}','1', """
            if request.GET.get('dept') :
                sql2 = f"""'{dept}'"""
            else:
                sql2 = f"""'{dept}'"""
            sql3 = f""" ,'summ','{curr_date}' """
            sql = sql1 + sql2 + sql3
            print(sql)
            cursor.execute(sql)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()

        context = {
            'data_list_dept' : data_list_dept,
            'month' : month,
            'year' : year,
            'dept' : dept,
            'data_list' : data_list,
            'month_list' : month_list,
            'year_list' : range(2021,curr_year+1)
        }
        return render(request, 'sampling_cost.html', context)
    
 
        