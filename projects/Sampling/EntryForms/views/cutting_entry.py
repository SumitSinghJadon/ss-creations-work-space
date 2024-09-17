from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import CommonMaster, FirstLevelMaster
from Sampling_db.models import CuttingEntryMt,CuttingTransactionDt
from django.contrib import messages
from Sampling_db.models import SampleBookingMt,SampleArticleDetails,SampleSizeQuantity
from IS_Nexus.database.sampling import get_merchant_by_merchant_head, get_style_by_buyer, get_season_year_by_season
from django.http import JsonResponse
from IS_Nexus.functions import queryset_to_json
from django.db import connections, connection
from IS_Nexus.functions.shortcuts import get_next_number,pay_db
from datetime import datetime , timedelta
from functions import cutter_name_list
from django.conf import settings

class CuttingEntryView(View):
    
    def get(self, request):
        intellisync_db = settings.DATABASES['intellisync_db']['NAME']
        booking_no              = SampleBookingMt.objects.filter(is_active=True,booking_status='confirm').values('id', 'booking_no')
        sample_type_list        = FirstLevelMaster.objects.filter(master_type__code='CM6', is_active=True)
        merchant_name_list      = CuttingEntryMt.objects.filter(is_active=True).values('id', 'booking_no')
        merchant_group_name_list= CommonMaster.objects.filter(master_type__code='CM22', is_active=True)
        buyer_list              = CommonMaster.objects.filter(master_type__code='buyer', is_active=True)

        flag = request.GET.get('flag')

        if flag == 'get_merchant_by_merchant_head':
            mid = request.GET.get('merchant_head')
            data = get_merchant_by_merchant_head(mid, fields=['name', 'value', 'id'])
            return JsonResponse(data, safe=False)
        
        elif flag == 'get_style_by_buyer':
            bid = request.GET.get('bid')
            data = get_style_by_buyer(bid, fields=['styleno'])
            return JsonResponse(data, safe=False)
        
        elif flag == 'get_season_year_by_season':
            sid = request.GET.get("sid")
            data = get_season_year_by_season(sid, fields=['name', 'id'])
            return JsonResponse(data, safe=False)
        
        elif flag == 'get_sample_type_by_sample_group':
            group_id = request.GET.get("sgt_id")
            data = FirstLevelMaster.objects.filter(master_type__code='CT-3', common_master=group_id, is_active=True).values('id', 'name').using('intellisync_db')
            data = queryset_to_json(data)
            return JsonResponse(data, safe=False)
        
        bid = request.GET.get('bid')
        mt_data = dt_data = None
        sq_data = ['1']
        samp_mt_data = []
        cutting_trans_list = []
        cursor =  connections['default'].cursor()

        if bid:
            sql = f""" delete from transaction_entry_mt where booking_id ='{bid}' and trans_type='cutting' """
            cursor.execute(sql)
            cursor.close()
            mt_data = SampleBookingMt.objects.get(id=bid)
            mt_data2 = SampleBookingMt.objects.filter(id=bid)
            dt_data = SampleArticleDetails.objects.filter(booking_id=mt_data)
            sq_data = SampleSizeQuantity.objects.filter(booking_id_id=bid)
            cutting_trans_list      = CuttingTransactionDt.objects.filter(booking_id=bid).values('id', 'transaction_no')
            # print(cutting_trans_list)
            cursor =  connections['default'].cursor()
            sql = f""" 
            select booking_no,booking_type,
            (CASE WHEN S.booking_type= 'F' THEN 'Fresh' WHEN S.booking_type= 'A' THEN 'Alter' WHEN S.booking_type= 'R' THEN 'Resubmission' END) booking_type_name,
            C3.name as sample_type,
            merchant_head_id,C1.name as merchant_head_name,merchant_name_id,C2.name as merchant_name,buyer_name,sample_type_id,
            style_no,season_year_id,C6.name as season_year,season_id,C4.name as season,booking_date,target_date,product_type_id,C5.name as product_type, 
            (select sum(quantity) samp_qty from sample_size_quantity where booking_id_id = s.id) samp_qty,
            STUFF((SELECT ','+ CAST(t.size as VARCHAR) FROM sample_size_quantity t WHERE booking_id_id= s.id  FOR XML PATH('')), 1, 1, '') sizes,
            c.qty as cut_qty,s.cut_assign_date
  
            from sample_booking_mt  s
            JOIN ( SELECT cm.id, cm.master_type_id, cm.name, cm.value, cm.code, cm.remark, cm.other, cm.is_active FROM {intellisync_db}.dbo.common_master cm INNER JOIN {intellisync_db}.dbo.common_master_type cmt ON (cm.master_type_id = cmt.id)  WHERE cm.is_active = 'True'  ) C1 ON C1.id = s.merchant_head_id
            JOIN (  select id,name from {intellisync_db}.dbo.first_level_master ) C2 ON C2.id = s.merchant_name_id
            JOIN (  select id,name from {intellisync_db}.dbo.first_level_master ) C3 ON C3.id = s.sample_type_id
            JOIN ( SELECT cm.id, cm.master_type_id, cm.name, cm.value, cm.code, cm.remark, cm.other, cm.is_active FROM {intellisync_db}.dbo.common_master cm INNER JOIN {intellisync_db}.dbo.common_master_type cmt ON (cm.master_type_id = cmt.id)  WHERE cm.is_active = 'True'  ) C4 ON C4.id = s.season_id
            JOIN ( SELECT cm.id, cm.master_type_id, cm.name, cm.value, cm.code, cm.remark, cm.other, cm.is_active FROM {intellisync_db}.dbo.common_master cm INNER JOIN {intellisync_db}.dbo.common_master_type cmt ON (cm.master_type_id = cmt.id)  WHERE cm.is_active = 'True'  ) C5 ON C5.id = s.product_type_id
            JOIN (  select id,name from {intellisync_db}.dbo.first_level_master ) C6 ON C6.id = s.season_year_id
            left join (select booking_id,SUM(qty) qty from cutting_entry_dt (nolock) where booking_id = '{bid}' group by booking_id )  c on s.id  =c.booking_id

            where s.id ='{bid}' """
            cursor.execute(sql)
            samp_mt_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            # samp_mt_data = cursor.fetchone()
            samp_mt_data = samp_mt_data[0] if samp_mt_data else None
            # print(samp_mt_data)
            cursor.close()
            
            sql_size = f"""
                select s.booking_id_id,s.size,s.color,sum(s.quantity) size_qty,
                ISNULL(c.qty,0) as total_cut_qty , ISNULL(( sum(s.quantity) - ISNULL(c.qty,0) ),0) balance_cut_qty
                from is_sampling_db.dbo.sample_size_quantity (nolock) s 
                left join (select booking_id,size,color,SUM(qty) qty from is_sampling_db.dbo.cutting_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s.booking_id_id  =c.booking_id and s.size = c.size and s.color = c.color
                where s.booking_id_id = '{bid}' and s.is_active='1'
                group by s.booking_id_id,s.size,s.color,c.qty 
                order by s.size,s.color asc
            """
            cursor=connections["payroll_db"].cursor()
            cursor.execute(sql_size)
            sq_data =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            # print(sq_data)
        curr_date = datetime.today().strftime('%Y-%m-%d')
        db_name = pay_db(curr_date)

        cutter_name_listt =  cutter_name_list()

        sql_size = f"""
            select dep_code,dep_name from om_01_24.dbo.tbdep where dep_code in 
            ( SELECT CAST(Item AS INTEGER) FROM is_app_db_new.dbo.split(( select CONDIDTION as dept_name from is_app_db_new.dbo.SystemParameters where ParameterName ='SAMP_DEPT' ), ',') )
        """
        cursor=connections["default"].cursor()
        cursor.execute(sql_size)
        sample_dept_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]

        merchant_head_list      = CommonMaster.objects.filter(master_type__code='CT-22', is_active=True).using('intellisync_db')
        merchant_list           = FirstLevelMaster.objects.filter(master_type__code='CT-23', is_active=True).using('intellisync_db')
        sample_type_master_list = FirstLevelMaster.objects.filter(master_type__code='CT-6', is_active=True).using('intellisync_db')
        sample_group_list       = CommonMaster.objects.filter(master_type__code='CT-2', is_active=True).using('intellisync_db')
        style_list              = CommonMaster.objects.filter(master_type__code='style', is_active=True).using('intellisync_db')
        season_list             = CommonMaster.objects.filter(master_type__code='CT-12', is_active=True).using('intellisync_db')
        product_type_list       = CommonMaster.objects.filter(master_type__code='CT-7', is_active=True).using('intellisync_db')
        article_list            = dt_data or FirstLevelMaster.objects.filter(master_type__code='CT-11', is_active=True).order_by('common_master__value', 'value').using('intellisync_db')
        
        context = {
            'booking_no'               : booking_no,
            'cutting_trans_list'       : cutting_trans_list,
            'sample_type_list'         : sample_type_list,
            'merchant_name_list'       : merchant_name_list,
            'merchant_group_name_list' : merchant_group_name_list,
            'buyer_list'               : buyer_list,
            
            "sample_type_master_list" : sample_type_master_list,
            "merchant_head_list"      : merchant_head_list,
            "merchant_list"           : merchant_list,
            "sample_group_list"       : sample_group_list,
            "style_list"              : style_list,
            "season_list"             : season_list,
            "product_type_list"       : product_type_list,
            "article_list"            : article_list,
            "mt_data"                 : mt_data,
            "dt_data"                 : dt_data,
            "sq_data"                 : sq_data,
            "samp_mt_data"            : samp_mt_data,
            "cutter_name_list"        : cutter_name_listt,
            "sample_dept_list"        : sample_dept_list,
            # "color_list"              : color_list,
        }
        return render(request, 'cutting_entry.html', context)
    
    def post(self, request):
        curr_user = request.user.id
        curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        # Fetch data from form
        booking_id           = request.POST.get('booking_no')
        cutting_type         = request.POST.get('cutting_type')
        cut_qty              = request.POST.get('cut_qty_val')
        size_breakup         = request.POST.get('size_breakup')
        cutter_name          = request.POST.get('cutter_name')
        assign_date          = request.POST.get('assign_date')
        handover_to_supervisor = request.POST.get('handover_to_supervisor')
        remarks                = request.POST.get('remarks')
        sample_status          = request.POST.get('sample_status')
        sample_dept          = request.POST.get('sample_dept')
        
        # Verify related data 
        booking_id = SampleBookingMt.objects.get(id=booking_id)
        
        transaction_no = get_next_number(CuttingTransactionDt,'CSMP')
        
        cutting_dt = CuttingTransactionDt.objects.create(
            booking_no = booking_id.booking_no,
            booking_id = booking_id,
            transaction_no = transaction_no, 
            cutting_type = cutting_type, 
            cut_qty = cut_qty ,
            size_breakup = size_breakup ,
            cutter_name = cutter_name ,
            assign_date = assign_date ,
            handover_to_supervisor = handover_to_supervisor ,
            remarks = remarks ,
            sample_status = sample_status,
            sample_dept = sample_dept,
            created_by = curr_user, 
            created_at = curr_date 
        )
        cursor =  connections['default'].cursor()
        sql_ins = f""" insert into cutting_entry_dt(qty,size,booking_no,booking_id,color,is_active,updated_at,created_at,cutting_dt,created_by) 
        (select qty,size,booking_no,booking_id,color,is_active,updated_at,created_at,{cutting_dt.id} as cutting_dt,created_by 
        from transaction_entry_mt where booking_id = {booking_id.id} and trans_type='cutting' )   """
        # print(sql_ins)
        cursor.execute(sql_ins)
        cursor.close()
        
        cursor =  connections['default'].cursor()
        sql_del = f""" delete from transaction_entry_mt where booking_id = {booking_id.id} and trans_type='cutting' """
        cursor.execute(sql_del)
        cursor.close()
                
        messages.success(request, "Success! The entry has been created.")
        return redirect ('cutting_entry_page')