from django.views import View
from django.shortcuts import render, redirect
from IntelliSync_db.models import CommonMaster, FirstLevelMaster
from Sampling_db.models import StitchEntryMt,StitchTransactionDt
from django.contrib import messages
from Sampling_db.models import SampleBookingMt,SampleArticleDetails,SampleSizeQuantity , CuttingTransactionDt
from IS_Nexus.database.sampling import get_merchant_by_merchant_head, get_style_by_buyer, get_season_year_by_season
from django.http import JsonResponse
from IS_Nexus.functions import queryset_to_json
from django.db import connections, connection
from IS_Nexus.functions.shortcuts import get_next_number
from datetime import datetime , timedelta
from functions import delete_unused_stitch_temp_trans , samp_booking_data , cutting_size_color_wise_qty , tailor_name_list , supervisor_name_list , checker_name_list


class StitchingEntryView(View):
    def get(self, request):
        booking_no              = CuttingTransactionDt.objects.filter(sample_status='O').values('booking_id', 'booking_no').distinct()
        # cutting_min_date        = CuttingTransactionDt.objects.filter(booking_no=booking_no).values('updated_at').distinct()
        sample_type_list        = FirstLevelMaster.objects.filter(master_type__code='CM6', is_active=True)
        merchant_name_list      = StitchEntryMt.objects.filter(is_active=True).values('id', 'booking_no')
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
        tailor_list = []
        sup_name_list = []
        checker_list = []

        if bid:
            delete_unused_stitch_temp_trans(bid)
            mt_data = SampleBookingMt.objects.get(id=bid)
            mt_data2 = SampleBookingMt.objects.filter(id=bid)
            dt_data = SampleArticleDetails.objects.filter(booking_id=mt_data)
            sq_data = SampleSizeQuantity.objects.filter(booking_id_id=bid)
            cutting_trans_list      = StitchTransactionDt.objects.filter(booking_id=bid).values('id', 'transaction_no')
            # print(cutting_trans_list)
            
            samp_mt_data = samp_booking_data(bid)
            # samp_mt_data = cursor.fetchone()
            sq_data = cutting_size_color_wise_qty(bid)
            # print(sq_data)
            curr_date = datetime.today().strftime('%Y-%m-%d')
            tailor_list =  tailor_name_list()
            sup_name_list =  supervisor_name_list()
            checker_list =  checker_name_list()
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
            "tailor_name_list"        : tailor_list,
            "sup_name_list"           : sup_name_list,
            "checker_name_list"        : checker_list,
            "sample_dept_list"        : sample_dept_list,
            # "color_list"              : color_list,
        }
        return render(request, 'stitching_transaction_entry.html', context)
    
    def post(self, request):
        # Fetch data from form
        curr_user = request.user.id
        curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        booking_id = request.POST.get('booking_no') 
        stitch_type = request.POST.get('stitch_type')
        stitch_qty = request.POST.get('stitch_qty_val')
        size_breakup = request.POST.get('size_breakup')
        tailor_name = request.POST.get('tailor_name')
        supervisor_name = request.POST.get('supervisor_name')
        checker_name = request.POST.get('checker_name')
        assign_date = request.POST.get('assign_date')
        handover_to_finish = request.POST.get('handover_to_finish')
        expected_time = request.POST.get('expected_time')
        taken_time = request.POST.get('taken_time')
        remarks = request.POST.get('remarks')
        stitch_status = request.POST.get('stitch_status')
        sample_dept          = request.POST.get('sample_dept')
        # Verify related data 
        booking_id = SampleBookingMt.objects.get(id=booking_id)
        
        transaction_no = get_next_number(StitchTransactionDt,'SSMP')
        try:
            stitch_dt = StitchTransactionDt.objects.create(
                booking_no = booking_id.booking_no,
                booking_id = booking_id, 
                transaction_no = transaction_no,
                stitch_type = stitch_type,
                stitch_qty = stitch_qty,
                size_breakup = size_breakup,
                tailor_name = tailor_name,
                supervisor_name = supervisor_name,
                checker_name = checker_name,
                assign_date = assign_date,
                handover_to_finish = handover_to_finish,
                expected_time = expected_time,
                taken_time = taken_time,
                remarks = remarks,
                stitch_status = stitch_status,
                sample_dept = sample_dept,
                created_by = curr_user,
                created_at = curr_date
            )
            try:
                cursor =  connections['default'].cursor()
                sql_ins = f""" insert into stitch_entry_dt(qty,size,booking_no,booking_id,color,is_active,updated_at,created_at,stitch_dt,created_by) 
                (select qty,size,booking_no,booking_id,color,is_active,updated_at,created_at,{stitch_dt.id} as stitch_dt,created_by 
                from transaction_entry_mt where booking_id = {booking_id.id} and trans_type='stitch' )  """
                # print(sql_ins)
                cursor.execute(sql_ins)
                cursor.close()
                
                cursor =  connections['default'].cursor()
                sql_del = f""" delete from transaction_entry_mt where booking_id = {booking_id.id} and trans_type='stitch' """
                cursor.execute(sql_del)
                cursor.close()
                        
                messages.success(request, "Success! The entry has been created.")
            except Exception as e:
                print(e)    
                stitch_dt.delete()
                messages.error(request, "Data Not Saved")
        except Exception as e:
            print(e)
            messages.error(request, "Data Not Saved")
        return redirect ('stitching_transaction_entry_page')