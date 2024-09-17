from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import CommonMaster, FirstLevelMaster
from Sampling_db.models import OtherEntryMt,OtherTransactionDt
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
from ERP_db.models import Party, Sizetype, Color

class OtherEntryView(View):
    
    def get(self, request):
        intellisync_db = settings.DATABASES['intellisync_db']['NAME']
        booking_no              = SampleBookingMt.objects.filter(is_active=True,booking_status='confirm').values('id', 'booking_no')
        sample_type_list        = FirstLevelMaster.objects.filter(master_type__code='CM6', is_active=True)
        merchant_name_list      = OtherEntryMt.objects.filter(is_active=True).values('id', 'booking_no')
        merchant_group_name_list= CommonMaster.objects.filter(master_type__code='CM22', is_active=True)
        # buyer_list              = CommonMaster.objects.filter(master_type__code='buyer', is_active=True)

        merchant_head_list = CommonMaster.objects.filter(master_type__code='CT-22', is_active=True).using('intellisync_db')
        buyer_list         = Party.objects.filter(active=1, isbuyer=1).values('party_code','party_name','pname').using('erp_db')
        sample_group_list  = CommonMaster.objects.filter(master_type__code='CT-4', is_active=True).using('intellisync_db')
        season_list        = CommonMaster.objects.filter(master_type__code='CT-12', is_active=True).using('intellisync_db')
        product_type_list  = CommonMaster.objects.filter(master_type__code='CT-7', is_active=True).using('intellisync_db')
        article_list       = dt_data or FirstLevelMaster.objects.filter(master_type__code='CT-11', is_active=True).order_by('common_master__value', 'value').using('intellisync_db')
        size_list          = Sizetype.objects.all().values('sizetypeid', 'sizetype')

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
        other_trans_list = []
        cursor =  connections['default'].cursor()
        
        curr_date = datetime.today().strftime('%Y-%m-%d')
        db_name = pay_db(curr_date)

        cutter_name_listt =  cutter_name_list()

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
            'other_trans_list'       : other_trans_list,
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
            # "size_list"               : size_list,
            # "color_list"              : color_list,
        }
        return render(request, 'other_transaction_entry.html', context)
    
    def post(self, request):
        curr_user = request.user.id
        curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # Fetch data from form
        booking_id           = request.POST.get('booking_no')
        other_type         = request.POST.get('other_type')
        cut_qty              = request.POST.get('cut_qty_val')
        size_breakup         = request.POST.get('size_breakup')
        cutter_name          = request.POST.get('cutter_name')
        assign_date          = request.POST.get('assign_date')
        handover_to_supervisor = request.POST.get('handover_to_supervisor')
        remarks                = request.POST.get('remarks')
        sample_status          = request.POST.get('sample_status')
        
        # Verify related data 
        booking_id = SampleBookingMt.objects.get(id=booking_id)
        
        transaction_no = get_next_number(OtherTransactionDt,'OSMP')
        
        other_dt = OtherTransactionDt.objects.create(
            booking_no = booking_id.booking_no,
            booking_id = booking_id,
            transaction_no = transaction_no, 
            other_type = other_type, 
            qty = cut_qty ,
            size_breakup = size_breakup ,
            cutter_name = cutter_name ,
            assign_date = assign_date ,
            handover_to_supervisor = handover_to_supervisor ,
            remarks = remarks ,
            sample_status = sample_status,
            created_by = curr_user, 
            created_at = curr_date 
        )
        cursor =  connections['default'].cursor()
        sql_ins = f""" insert into other_entry_dt(qty,size,booking_no,booking_id,color,is_active,updated_at,created_at,other_dt,created_by) 
        (select qty,size,booking_no,booking_id,color,is_active,updated_at,created_at,{other_dt.id} as other_dt,created_by 
        from transaction_entry_mt where booking_id = {booking_id.id} and trans_type='other' )   """
        # print(sql_ins)
        cursor.execute(sql_ins)
        cursor.close()
        
        cursor =  connections['default'].cursor()
        sql_del = f""" delete from transaction_entry_mt where booking_id = {booking_id.id} and trans_type='other' """
        cursor.execute(sql_del)
        cursor.close()
                
        messages.success(request, "Success! The entry has been created.")
        return redirect ('other_transaction_entry_page')