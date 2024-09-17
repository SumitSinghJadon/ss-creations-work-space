from django.views import View
from django.shortcuts import render
from django.db.models import CharField, Value, functions, F, aggregates
from django.db.models.functions import Concat
from django.db import connections
from django.contrib import messages
from datetime import datetime , timedelta
from Sampling_db.models import SampleBookingMt
from IS_Nexus.functions.shortcuts import get_next_number,pay_db
from django.conf import settings

class ConcatAgg(aggregates.Aggregate):
    function = 'STRING_AGG'
    template = "%(function)s(%(distinct)s%(expressions)s, '')"
    allow_distinct = True


class SampleStatusView(View):
    def get(self, request):
        intellisync_db = settings.DATABASES['intellisync_db']['NAME']
        if request.GET.get('from_date') and request.GET.get('to_date'):
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
        else:
             from_date = datetime.today().strftime('%Y-%m-01')
             to_date = datetime.today().strftime('%Y-%m-%d')
        if request.GET.get('buyer'):
            buyer = request.GET.get('buyer')
        else:
            buyer =''
        curr_date = datetime.today().strftime('%Y-%m-%d')
        db_name = pay_db(curr_date)
        buyer_list = SampleBookingMt.objects.filter(is_active=True).values('buyer_name', 'buyer_code').order_by('buyer_name').distinct()
        cursor =  connections['default'].cursor()
        sql_cutter1 = f"""
        select c.name as sample_group,s.booking_no,mh.name as Merchant_head,m.name as Merchant_name, 
        (CASE WHEN booking_type ='F' THEN 'Fresh' WHEN booking_type ='A' THEN 'Alter' WHEN booking_type ='R' THEN 'Resubmission' END) booking_type,buyer_name,style_no,
        sy.name as season_year, st.name as sample_type,total_qty, CONVERT(varchar, booking_date, 3) booking_date, CONVERT(varchar, file_rcv_date, 3) file_rcv_date,
        CONVERT(varchar, target_date, 3) target_date,DATEDIFF(DD, CONVERT(varchar, booking_date, 23) , CONVERT(varchar, file_rcv_date, 23) ) as sample_lead_time,s.booking_status as sample_status, 
        CONVERT(varchar, f.finish_date, 3) as sample_handover_date,
        DATEDIFF(DD, CONVERT(varchar, target_date, 23) , CONVERT(varchar, f.finish_date, 23) ) as actual_lead_time,
        '' as final_status,
        s.booking_hold_reason as hold_reason, s.article_reject_reason as reject_reason,remarks,f.qa_status as qa_status,f.qa_remarks as qa_remarks,
        '' as merchant_remarks,
        d.dispatch_status as handover_status ,
        '' as merchant_status_remarks
        from sample_booking_mt s
        join (select id,name from {intellisync_db}.dbo.common_master group by id,name ) c on c.id =  s.sample_group_type_id
        join (select id,name from {intellisync_db}.dbo.first_level_master group by id,name) st on st.id = s.sample_type_id
        join (select id,name from {intellisync_db}.dbo.common_master group by id,name ) p on p.id =  s.product_type_id
        join (select id,name from {intellisync_db}.dbo.common_master group by id,name ) mh on mh.id =  s.merchant_head_id
        join (select id,name from {intellisync_db}.dbo.first_level_master group by id,name) m on m.id = s.merchant_name_id
        join (select id,name from {intellisync_db}.dbo.first_level_master group by id,name) sy on sy.id = s.season_year_id
        left join (select qa_remarks, (CASE WHEN qa_status = 'O' THEN 'OK' ELSE qa_status END) qa_status, booking_no,booking_id,MAX(convert(varchar,CAST(replace(return_date,'T',' ') as DATETIME),23)) return_date,max(cast(created_at as date)) finish_date from finish_entry_mt group by qa_remarks, qa_status ,booking_no,booking_id) f on f.booking_no = s.booking_no
        left join (select booking_no,booking_id,convert(varchar,max(cast(created_at as date)),23) dispatch_date,'Done' as dispatch_status from dispatch_entry_mt group by booking_no,booking_id) d on d.booking_no = s.booking_no

        where CONVERT(varchar, booking_date, 23) between '{from_date}' and '{to_date}'
        
        """
        if request.GET.get('buyer'):
            sql_cutter2 = f""" and s.buyer_code ='{buyer}'  """
        else:
            sql_cutter2 = f"""  """

        sql_cutter3 = f""" order by c.name,booking_type,m.name,s.booking_no asc  """
        
        sql_cutter = sql_cutter1 + sql_cutter2 + sql_cutter3
        # and booking_date between '{from_date}' and '{to_date}'
        # print(sql_cutter)
        cursor.execute(sql_cutter)
        data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        context = {
            'buyer' : buyer,
            'buyer_list' : buyer_list,
            'data_list' : data_list,
            'from_date' : from_date,
            'to_date' : to_date,
        }
        return render(request, 'sample_status.html', context)
    
 
        