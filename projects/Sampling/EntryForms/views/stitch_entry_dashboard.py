from django.views import View
from django.shortcuts import render
from django.db.models import CharField, Value, functions, F, aggregates
from django.db.models.functions import Concat
from django.db import connections
from django.contrib import messages
from datetime import datetime , timedelta
from IS_Nexus.functions.shortcuts import get_next_number,pay_db
from django.conf import settings

class ConcatAgg(aggregates.Aggregate):
    function = 'STRING_AGG'
    template = "%(function)s(%(distinct)s%(expressions)s, '')"
    allow_distinct = True


class StitchDashboardView(View):
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
            select s.id as samp_id,c.id as trans_id,s.booking_no,c.transaction_no,s.buyer_name,s.style_no,C3.name as sample_type,
            (case WHEN c.stitch_type ='1' THEN 'Fresh' WHEN c.stitch_type ='2' THEN 'Alter' WHEN c.stitch_type ='3' THEN 'Recut' end) stitch_type,
            c.size_breakup as stitch_size,c.stitch_qty,
            t.emp_name as tailor_name,c.assign_date as stitch_date,
            (select ISNULL(sum(qty),0) audit_count from stitch_entry_size_dt where trans_id = c.id) audit_count 
            from sample_booking_mt (nolock) s join stitch_entry_mt (nolock) c on s.id = c.booking_id 
            left join {db_name}.dbo.tbemp (nolock) t on c.tailor_name =  t.emp_paycode
            JOIN (select id,name from [is_intellisync_db].dbo.first_level_master ) C3 ON C3.id = s.sample_type_id
            where s.is_active ='1' 
            order by s.id,c.id
        """
        # and booking_date between '{from_date}' and '{to_date}'
        # print(sql_cutter)
        cursor.execute(sql_cutter)
        stitch_trans_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        context = {
            'stitch_trans_list' : stitch_trans_list,
        }
        return render(request, 'stitch_entry_dashboard.html', context)
    
 
        