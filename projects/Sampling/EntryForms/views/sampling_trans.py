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


class SamplingTransView(View):
    def get(self, request):

        bid = request.GET.get('bid')
        trans_type = request.GET.get('trans_type')
        # style = request.GET.get('style')

        curr_date = datetime.today().strftime('%Y-%m-%d')
        curr_year = int(datetime.today().strftime('%Y'))
        db_name = pay_db(curr_date)


        if trans_type and bid:
            cursor = connections['default'].cursor()
            sql1 = f"""    EXEC GET_SAMP_REPORTS 'sample_trans',NULL,NULL,'{trans_type}','{bid}'  """
            sql = sql1
            print(sql)
            cursor.execute(sql)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()

        context = {
            'trans_type' : trans_type,
            'bid' : bid,
            'data_list' : data_list,
            'year_list' : range(2021,curr_year+1)
        }
        return render(request, 'sampling_trans.html', context)
    
 
        