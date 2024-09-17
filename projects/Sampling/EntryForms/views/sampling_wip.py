from django.views import View
from django.shortcuts import render
from django.db.models import CharField, Value, functions, F, aggregates
from django.db.models.functions import Concat
from django.db import connections
from django.contrib import messages
from datetime import datetime , timedelta
from IS_Nexus.functions.shortcuts import get_next_number,pay_db

class ConcatAgg(aggregates.Aggregate):
    function = 'STRING_AGG'
    template = "%(function)s(%(distinct)s%(expressions)s, '')"
    allow_distinct = True


class SamplingWIPView(View):
    def get(self, request):
        curr_date = datetime.today().strftime('%Y-%m-%d')
        db_name = pay_db(curr_date)
        if request.GET.get('from_date') and request.GET.get('to_date'):
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
        else:
             from_date = datetime.today().strftime('%Y-%m-01')
             to_date = datetime.today().strftime('%Y-%m-%d')

        if request.GET.get('active_status'):
            active_status = request.GET.get('active_status')
        else:
            active_status = '' 

        if request.GET.get('samp_dept'):
            samp_dept = request.GET.get('samp_dept')
        else:
            samp_dept = '' 

        cursor = connections['is_app'].cursor()
        sqldp = f"""  select CONDIDTION from SystemParameters where ParameterName ='SAMP_DEPT' """
        cursor.execute(sqldp)
        dept_list_arr =  cursor.fetchone()
        cursor.close()
        dept_list = dept_list_arr[0]
            
        cursor = connections['default'].cursor()
        sql = f""" 
            select dep_code,dep_name from {db_name}.dbo.tbdep where dep_code in ({dept_list}) order by dep_name asc
        """
        cursor.execute(sql)
        data_list_dept =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        cursor.close()


        cursor =  connections['default'].cursor()
        if from_date and to_date:
            cursor = connections['default'].cursor()
            sql1 = f""" 
                EXEC GET_SAMPLING_WIP '{from_date}','{to_date}','booking',
            """
            if request.GET.get('active_status'):
                sql2 = f""" '{active_status}',  """
            else:
                sql2 = f""" NULL,  """

            if request.GET.get('samp_dept'):
                sql3 = f""" '{samp_dept}'  """
            else:
                sql3 = f""" NULL  """
            
            sql = sql1 + sql2 + sql3 
            cursor.execute(sql)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        context = {
            'data_list_dept' : data_list_dept,
            'samp_dept' : samp_dept,
            'active_status' : active_status,
            'data_list' : data_list,
            'from_date' : from_date,
            'to_date' : to_date
        }
        return render(request, 'sampling_wip.html', context)
    
 
        