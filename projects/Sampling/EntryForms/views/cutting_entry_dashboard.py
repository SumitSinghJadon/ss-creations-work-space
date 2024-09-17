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


class CuttingDashboardView(View):
    def get(self, request):

        if request.GET.get('from_date') and request.GET.get('to_date'):
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
        else:
             from_date = datetime.today().strftime('%Y-%m-01')
             to_date = datetime.today().strftime('%Y-%m-%d')

        curr_date = datetime.today().strftime('%Y-%m-%d')
        db_name = pay_db(curr_date)
        cursor =  connections['default'].cursor()
        sql_cutter = f"""
        select s.id,c.id,s.booking_no,c.transaction_no,s.buyer_name,s.style_no,C3.name as sample_type,
        (case WHEN c.cutting_type ='1' THEN 'Fresh' WHEN c.cutting_type ='2' THEN 'Alter' WHEN c.cutting_type ='3' THEN 'Recut' end) cutting_type,
        c.size_breakup as cutting_size,c.cut_qty as cut_qty,
        t.emp_name as cutter_name,c.assign_date as cutting_date 
        from sample_booking_mt (nolock) s join cutting_entry_mt (nolock) c on s.id = c.booking_id 
        left join {db_name}.dbo.tbemp (nolock) t on c.cutter_name =  t.emp_paycode
        JOIN (  select id,name from [is_intellisync_db].dbo.first_level_master ) C3 ON C3.id = s.sample_type_id
        where s.is_active ='1' 

        order by c.id desc
        """
        # and booking_date between '{from_date}' and '{to_date}'
        # print(sql_cutter)
        cursor.execute(sql_cutter)
        cutting_trans_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        context = {
            'cutting_trans_list' : cutting_trans_list,
        }
        return render(request, 'cutting_entry_dashboard.html', context)
    
 
        