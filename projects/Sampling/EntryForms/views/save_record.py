from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages as msg
from IS_Nexus.functions import messages,queryset_to_json
from django.db import connections, connection
from Sampling_db.models import SampleBookingMt,SampleArticleDetails,SampleSizeQuantity,CuttingEntryMt
from django.conf import settings


class SaveRecordView(View):
    def get(self, request):
        curr_user = request.user.id
        intellisync_db = settings.DATABASES['intellisync_db']['NAME']
        print(request.build_absolute_uri(),'\n\n')
        flag = request.GET.get('flag')

        if flag == 'save_cutting_qty': 
            booking_list  = request.GET.getlist('booking_id')
            size_list     = request.GET.getlist('size')
            color_list    = request.GET.getlist('color')
            balance_cut_qty_list = request.GET.getlist('balance_cut_qty')
            quantity_list = request.GET.getlist('cut_qty')
            tra_id_list = request.GET.getlist('tra_id')
            total_qty =0
            size_breakup =''
            return_arr = []
            curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            for booking_id,size, color,balance_cut_qty, quantity , tra_id in zip(booking_list,size_list, color_list,balance_cut_qty_list, quantity_list , tra_id_list):
                bid  = booking_id
                booking_id = SampleBookingMt.objects.get(id=booking_id)
                cursor =  connections['default'].cursor()
                sql = f""" 
                select s.id,s1.quantity as sample_qty,isnull(sum(c.qty),0) as cut_qty,isnull(( s1.quantity - isnull(sum(c.qty),0) ),0) balance_qty 
                from (select id,total_qty from sample_booking_mt ) s 
                join sample_size_quantity s1 on s.id  = s1.booking_id_id
                left join cutting_entry_dt c on s1.booking_id_id = c.booking_id and s1.size= c.size and s1.color = c.color
                where s.id ={bid} and s1.size='{size}' and s1.color ='{color}'
                group by s.id,s1.quantity               
                """
                cursor.execute(sql)
                cut_mt_data = cursor.fetchone()
                cursor.close()
                # int(cut_mt_data['balance_qty'])
                if size and color and int(quantity) > 0 and cut_mt_data[3] >= int(quantity):
                    total_qty = total_qty + int(quantity)
                    size_breakup =  size + ',' + size_breakup 
                    cursor =  connections['default'].cursor()
                    
                    if int(tra_id) > 0 :
                        sql = f""" 
                        update transaction_entry_mt set qty = {quantity},updated_by={curr_user} where booking_id ='{bid}' and size='{size}' and color ='{color}' and trans_type ='cutting' and id='{tra_id}'
                        """ 
                    else :    
                        sql = f""" 
                        insert into transaction_entry_mt (qty,size,is_active,updated_at,created_at,booking_no,booking_id,color,trans_type,created_by) 
                        values('{quantity}','{size}',1,'{curr_date_time}','{curr_date_time}','{booking_id}',{bid},'{color}','cutting','{curr_user}')                
                        """
                    # print(sql)
                    cursor.execute(sql)
                    cursor.close()
                    size_breakup =  size_breakup.rstrip(',')
            return_arr = {"total_qty" : total_qty, "size_breakup": size_breakup}

            return JsonResponse(return_arr,safe=False)   
        
        elif flag == 'save_stitch_qty': 
            booking_list     = request.GET.getlist('booking_id')
            size_list     = request.GET.getlist('size')
            color_list    = request.GET.getlist('color')
            balance_cut_qty_list    = request.GET.getlist('balance_stitch_qty')
            quantity_list = request.GET.getlist('stitch_qty')
            tra_id_list = request.GET.getlist('tra_id')
            total_qty =0
            size_breakup =''
            return_arr = []
            curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for booking_id,size, color,balance_cut_qty, quantity, tra_id in zip(booking_list,size_list, color_list,balance_cut_qty_list, quantity_list , tra_id_list):
                bid  = booking_id
                booking_id = SampleBookingMt.objects.get(id=booking_id)
                cursor =  connections['default'].cursor()
                sql = f""" 
                    select s.id,s1.quantity as sample_qty,isnull(sum(c1.qty),0) as cut_qty,isnull(st.qty,0) as stitch_qty, isnull(( isnull(sum(c1.qty),0) - isnull(st.qty,0) ),0) balance_qty 
                    from (select id,total_qty from sample_booking_mt ) s 
                    join sample_size_quantity s1 on s.id  = s1.booking_id_id
                    join cutting_entry_dt c1 on s1.booking_id_id = c1.booking_id and s1.size= c1.size and s1.color = c1.color
                    left join (select booking_id,size,color,SUM(qty) qty from stitch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  st on s1.booking_id_id  =st.booking_id and s1.size = st.size and s1.color = st.color

                    where s.id ={bid} and s1.size='{size}' and s1.color ='{color}'
                    group by s.id,s1.quantity,st.qty
                """
                # print(sql)
                cursor.execute(sql)
                stitch_mt_data = cursor.fetchone()
                # print(stitch_mt_data)
                cursor.close()
                # int(stitch_mt_data['balance_qty'])
                if size and color and int(quantity) > 0 and stitch_mt_data[4] >= int(quantity):
                    total_qty = total_qty + int(quantity)
                    size_breakup =  size + ',' + size_breakup 
                    cursor =  connections['default'].cursor()
                    
                    if int(tra_id) > 0 :
                        sql = f"""update transaction_entry_mt set qty = {quantity},updated_by={curr_user} where booking_id ='{bid}' and size='{size}' and color ='{color}' and trans_type ='stitch' and id='{tra_id}'""" 
                    else :    
                        sql = f"""INSERT into transaction_entry_mt (qty,size,is_active,updated_at,created_at,booking_no,booking_id,color,trans_type,created_by) 
                        values('{quantity}','{size}',1,'{curr_date_time}','{curr_date_time}','{booking_id}',{bid},'{color}','stitch','{curr_user}')                
                        """
                    # print(sql)
                    cursor.execute(sql)
                    cursor.close()
                    size_breakup =  size_breakup.rstrip(',')
            return_arr = {"total_qty" : total_qty, "size_breakup": size_breakup}

            return JsonResponse(return_arr,safe=False)   

        elif flag == 'save_stitch_defect': 
                ctype     = request.GET.get('ctype')
                qid     = request.GET.get('qid')
                color     = request.GET.get('color')
                size     = request.GET.get('size')
                trans_id     = request.GET.get('trans_id')
                defect_id    = request.GET.get('defect_id')
                defect_type         = request.GET.get('defect_type')
                total_count = 0 
                total_count_qid = 0 
                total_count_all = 0 
                curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                cursor =  connections['default'].cursor()
                if ctype == 'add':
                    sql = f""" 
                    insert into defect_transaction_entry_mt (color,size,qid,qty,is_active,updated_at,created_at,defect_type,trans_type,defect_id,trans_id,created_by) 
                    values('{color}','{size}','{qid}','1',1,'{curr_date_time}','{curr_date_time}','{defect_type}','stitch','{defect_id}','{trans_id}','{curr_user}')
                    """
                elif ctype == 'remove':
                    sql = f"""
                    delete from defect_transaction_entry_mt where color ='{color}' and size = '{size}' and qid = '{qid}' and defect_type = '{defect_type}' and trans_type = 'stitch' and defect_id = '{defect_id}' and trans_id = '{trans_id}'
                    and id = (select top 1 id from defect_transaction_entry_mt where color ='{color}' and size = '{size}' and qid = '{qid}' and defect_type = '{defect_type}' and trans_type = 'stitch' and defect_id = '{defect_id}' and trans_id = '{trans_id}' order by id desc)
                    """
                # print(sql)
                cursor.execute(sql)
                
                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' and defect_id = '{defect_id}' and defect_type = '{defect_type}' and trans_type ='stitch' and size= '{size}' and color ='{color}' and qid ='{qid}'   """
                # print(sql)
                cursor.execute(sql)
                stitch_defect_data = cursor.fetchone()
                total_count = stitch_defect_data[0]

                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' and defect_type = '{defect_type}' and trans_type ='stitch' and size= '{size}' and color ='{color}' and qid ='{qid}'  """
                # print(sql)
                cursor.execute(sql)
                stitch_defect_data_qid = cursor.fetchone()
                total_count_qid = stitch_defect_data_qid[0]

                sql = f""" 
                select t.trans_id,t.size,t.color,t.qid,COUNT(*) dd,
                STUFF(
                (select  DISTINCT ', ' + CONCAT( c1.name,'(',COUNT(*),')' ) from defect_transaction_entry_mt t1 
                join {intellisync_db}.dbo.first_level_master c1 on t1.defect_id = c1.id
                where trans_id = t.trans_id and size = t.size and qid = t.qid and color = t.color group by c1.name FOR XML PATH ('')) , 1, 1, '')  AS def_list
                from defect_transaction_entry_mt t where trans_id ='{trans_id}' and size = '{size}' and qid = '{qid}' and color = '{color}'
                group by t.trans_id,t.size,t.color,t.qid  
                """
                # print(sql)
                cursor.execute(sql)
                stitch_defect_data_list = cursor.fetchone()
                # print(stitch_defect_data_list)
                total_count_list = stitch_defect_data_list[5]
                               
                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' 
                and defect_type = '{defect_type}' and trans_type ='stitch'  """
                # print(sql)
                cursor.execute(sql)
                stitch_defect_data = cursor.fetchone()
                total_count_all = stitch_defect_data[0]
                
                cursor.close()
                
                return_arr = { "total_count_list" : total_count_list , "total_count_qid" : total_count_qid,"total_count_all" : total_count_all, "total_count" : total_count, "defect_type": defect_type}

                return JsonResponse(return_arr,safe=False)           

        elif flag == 'save_finish_qty': 
            booking_list     = request.GET.getlist('booking_id')
            size_list     = request.GET.getlist('size')
            color_list    = request.GET.getlist('color')
            balance_cut_qty_list    = request.GET.getlist('balance_finish_qty')
            quantity_list = request.GET.getlist('finish_qty')
            tra_id_list = request.GET.getlist('tra_id')
            total_qty =0
            size_breakup =''
            return_arr = []
            curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for booking_id,size, color,balance_cut_qty, quantity, tra_id in zip(booking_list,size_list, color_list,balance_cut_qty_list, quantity_list, tra_id_list):
                bid  = booking_id
                booking_id = SampleBookingMt.objects.get(id=booking_id)
                cursor =  connections['default'].cursor()
                sql = f""" 
                    select s.id,s1.quantity as sample_qty,isnull(sum(c1.qty),0) as stitch_qty,isnull(c.qty,0) as finish_qty,
                    isnull(( isnull(sum(c1.qty),0) - isnull(c.qty,0) ),0) balance_qty 
                    from (select id,total_qty from sample_booking_mt ) s 
                    join sample_size_quantity s1 on s.id  = s1.booking_id_id
                    join stitch_entry_dt c1 on s1.booking_id_id = c1.booking_id and s1.size= c1.size and s1.color = c1.color
                    left join (select booking_id,size,color,SUM(qty) qty from finish_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s1.booking_id_id  =c.booking_id and s1.size = c.size and s1.color = c.color

                    where s.id ={bid} and s1.size='{size}' and s1.color ='{color}'
                    group by s.id,s1.quantity,c.qty
                """
                # print(sql)
                cursor.execute(sql)
                finish_mt_data = cursor.fetchone()
                # print(finish_mt_data)
                cursor.close()
                # int(finish_mt_data['balance_qty'])
                if size and color and int(quantity) > 0 and finish_mt_data[4] >= int(quantity):
                    total_qty = total_qty + int(quantity)
                    size_breakup =  size + ',' + size_breakup 
                    cursor =  connections['default'].cursor()
                    # sql_chk = f""" select * from transaction_entry_mt where booking_id ='{bid}' and size='{size}' and color ='{color}' and trans_type ='finish'  """
                    # cursor.execute(sql_chk)
                    # trans_chk = cursor.fetchone()
                    if int(tra_id) > 0 :
                        sql = f""" 
                        update transaction_entry_mt set qty = {quantity},updated_by={curr_user} where booking_id ='{bid}' and size='{size}' and color ='{color}' and trans_type ='finish' and id='{tra_id}'
                        """ 
                    else :    
                        sql = f""" 
                        insert into transaction_entry_mt (qty,size,is_active,updated_at,created_at,booking_no,booking_id,color,trans_type,created_by) 
                        values('{quantity}','{size}',1,'{curr_date_time}','{curr_date_time}','{booking_id}',{bid},'{color}','finish','{curr_user}')                
                        """
                    # print(sql)
                    cursor.execute(sql)
                    cursor.close()
                    size_breakup =  size_breakup.rstrip(',')
            return_arr = {"total_qty" : total_qty, "size_breakup": size_breakup}

            return JsonResponse(return_arr,safe=False)   

        elif flag == 'save_finish_defect': 
                ctype     = request.GET.get('ctype')
                qid     = request.GET.get('qid')
                color     = request.GET.get('color')
                size     = request.GET.get('size')
                trans_id     = request.GET.get('trans_id')
                defect_id    = request.GET.get('defect_id')
                defect_type         = request.GET.get('defect_type')
                total_count = 0 
                total_count_qid = 0 
                total_count_all = 0 
                curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                cursor =  connections['default'].cursor()
                if ctype == 'add':
                    sql = f""" 
                        insert into defect_transaction_entry_mt (color,size,qid,qty,is_active,updated_at,created_at,defect_type,trans_type,defect_id,trans_id,created_by) 
                        values('{color}','{size}','{qid}','1',1,'{curr_date_time}','{curr_date_time}','{defect_type}','finish','{defect_id}','{trans_id}','{curr_user}')
                        """
                elif ctype == 'remove':
                    sql = f"""
                    delete from defect_transaction_entry_mt where color ='{color}' and size = '{size}' and qid = '{qid}' and defect_type = '{defect_type}' and trans_type = 'finish' and defect_id = '{defect_id}' and trans_id = '{trans_id}'
                    and id = (select top 1 id from defect_transaction_entry_mt where color ='{color}' and size = '{size}' and qid = '{qid}' and defect_type = '{defect_type}' and trans_type = 'finish' and defect_id = '{defect_id}' and trans_id = '{trans_id}' order by id desc)
                    """
                # print(sql)
                cursor.execute(sql)
                
                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' and defect_id = '{defect_id}' and defect_type = '{defect_type}' and trans_type ='finish' and size= '{size}' and color ='{color}' and qid ='{qid}'   """
                # print(sql)
                cursor.execute(sql)
                finish_defect_data = cursor.fetchone()
                total_count = finish_defect_data[0]

                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' and defect_type = '{defect_type}' and trans_type ='finish' and size= '{size}' and color ='{color}' and qid ='{qid}'  """
                # print(sql)
                cursor.execute(sql)
                finish_defect_data_qid = cursor.fetchone()
                total_count_qid = finish_defect_data_qid[0]

                sql = f""" 
                select t.trans_id,t.size,t.color,t.qid,COUNT(*) dd,
                STUFF(
                (select  DISTINCT ', ' + CONCAT( c1.name,'(',COUNT(*),')' ) from defect_transaction_entry_mt t1 
                join {intellisync_db}.dbo.first_level_master c1 on t1.defect_id = c1.id
                where trans_id = t.trans_id and size = t.size and qid = t.qid and color = t.color group by c1.name FOR XML PATH ('')) , 1, 1, '')  AS def_list
                from defect_transaction_entry_mt t where trans_id ='{trans_id}' and size = '{size}' and qid = '{qid}' and color = '{color}'
                group by t.trans_id,t.size,t.color,t.qid  
                """
                # print(sql)
                cursor.execute(sql)
                finish_defect_data_list = cursor.fetchone()
                # print(finish_defect_data_list)
                total_count_list = finish_defect_data_list[5]
                               
                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' 
                and defect_type = '{defect_type}' and trans_type ='finish'  """
                # print(sql)
                cursor.execute(sql)
                finish_defect_data = cursor.fetchone()
                total_count_all = finish_defect_data[0]
                
                cursor.close()
                
                return_arr = { "total_count_list" : total_count_list , "total_count_qid" : total_count_qid,"total_count_all" : total_count_all, "total_count" : total_count, "defect_type": defect_type}

                return JsonResponse(return_arr,safe=False) 


        elif flag == 'save_dispatch_qty': 
            booking_list     = request.GET.getlist('booking_id')
            size_list     = request.GET.getlist('size')
            color_list    = request.GET.getlist('color')
            balance_cut_qty_list    = request.GET.getlist('balance_dispatch_qty')
            quantity_list = request.GET.getlist('dispatch_qty')
            tra_id_list = request.GET.getlist('tra_id')
            total_qty =0
            size_breakup =''
            return_arr = []
            curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for booking_id,size, color,balance_cut_qty, quantity , tra_id in zip(booking_list,size_list, color_list,balance_cut_qty_list, quantity_list, tra_id_list):
                bid  = booking_id
                booking_id = SampleBookingMt.objects.get(id=booking_id)
                cursor =  connections['default'].cursor()
                sql = f""" 
                    select s.id,s1.quantity as sample_qty,isnull(sum(c1.qty),0) as finish_qty,isnull(c.qty,0) as dispatch_qty,
                    isnull(( isnull(sum(c1.qty),0) - isnull(c.qty,0) ),0) balance_qty 
                    from (select id,total_qty from sample_booking_mt ) s 
                    join sample_size_quantity s1 on s.id  = s1.booking_id_id
                    join finish_entry_dt c1 on s1.booking_id_id = c1.booking_id and s1.size= c1.size and s1.color = c1.color
                    left join (select booking_id,size,color,SUM(qty) qty from dispatch_entry_dt (nolock) where booking_id = '{bid}' group by booking_id,size,color )  c on s1.booking_id_id  =c.booking_id and s1.size = c.size and s1.color = c.color

                    where s.id ={bid} and s1.size='{size}' and s1.color ='{color}'
                    group by s.id,s1.quantity,c.qty
                """
                # print(sql)
                cursor.execute(sql)
                dispatch_mt_data = cursor.fetchone()
                # print(dispatch_mt_data)
                cursor.close()
                # int(dispatch_mt_data['balance_qty'])
                if size and color and int(quantity) > 0 and dispatch_mt_data[4] >= int(quantity):
                    total_qty = total_qty + int(quantity)
                    size_breakup =  size + ',' + size_breakup 
                    cursor =  connections['default'].cursor()
                    
                    if int(tra_id) > 0 :
                        sql = f""" 
                        update transaction_entry_mt set qty = {quantity},updated_by={curr_user} where booking_id ='{bid}' and size='{size}' and color ='{color}' and trans_type ='dispatch' and id='{tra_id}'
                        """ 
                    else :    
                        sql = f""" 
                        insert into transaction_entry_mt (qty,size,is_active,updated_at,created_at,booking_no,booking_id,color,trans_type,created_by) 
                        values('{quantity}','{size}',1,'{curr_date_time}','{curr_date_time}','{booking_id}',{bid},'{color}','dispatch','{curr_user}')                
                        """
                    # print(sql)
                    cursor.execute(sql)
                    cursor.close()
                    size_breakup =  size_breakup.rstrip(',')
            return_arr = {"total_qty" : total_qty, "size_breakup": size_breakup}

            return JsonResponse(return_arr,safe=False)   

        elif flag == 'save_dispatch_defect': 
                ctype     = request.GET.get('ctype')
                qid     = request.GET.get('qid')
                color     = request.GET.get('color')
                size     = request.GET.get('size')
                trans_id     = request.GET.get('trans_id')
                defect_id    = request.GET.get('defect_id')
                defect_type         = request.GET.get('defect_type')
                total_count = 0 
                total_count_qid = 0 
                total_count_all = 0 
                curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                cursor =  connections['default'].cursor()

                if ctype == 'add':
                    sql = f""" 
                    insert into defect_transaction_entry_mt (color,size,qid,qty,is_active,updated_at,created_at,defect_type,trans_type,defect_id,trans_id,created_by) 
                    values('{color}','{size}','{qid}','1',1,'{curr_date_time}','{curr_date_time}','{defect_type}','dispatch','{defect_id}','{trans_id}','{curr_user}')
                    """
                elif ctype == 'remove':
                    sql = f"""
                    delete from defect_transaction_entry_mt where color ='{color}' and size = '{size}' and qid = '{qid}' and defect_type = '{defect_type}' and trans_type = 'dispatch' and defect_id = '{defect_id}' and trans_id = '{trans_id}'
                    and id = (select top 1 id from defect_transaction_entry_mt where color ='{color}' and size = '{size}' and qid = '{qid}' and defect_type = '{defect_type}' and trans_type = 'dispatch' and defect_id = '{defect_id}' and trans_id = '{trans_id}' order by id desc)
                    """
                # print(sql)
                cursor.execute(sql)
                
                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' and defect_id = '{defect_id}' and defect_type = '{defect_type}' and trans_type ='dispatch' and size= '{size}' and color ='{color}' and qid ='{qid}'   """
                # print(sql)
                cursor.execute(sql)
                dispatch_defect_data = cursor.fetchone()
                total_count = dispatch_defect_data[0]

                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' and defect_type = '{defect_type}' and trans_type ='dispatch' and size= '{size}' and color ='{color}' and qid ='{qid}'  """
                # print(sql)
                cursor.execute(sql)
                dispatch_defect_data_qid = cursor.fetchone()
                total_count_qid = dispatch_defect_data_qid[0]

                sql = f""" 
                select t.trans_id,t.size,t.color,t.qid,COUNT(*) dd,
                STUFF(
                (select  DISTINCT ', ' + CONCAT( c1.name,'(',COUNT(*),')' ) from defect_transaction_entry_mt t1 
                join {intellisync_db}.dbo.first_level_master c1 on t1.defect_id = c1.id
                where trans_id = t.trans_id and size = t.size and qid = t.qid and color = t.color group by c1.name FOR XML PATH ('')) , 1, 1, '')  AS def_list
                from defect_transaction_entry_mt t where trans_id ='{trans_id}' and size = '{size}' and qid = '{qid}' and color = '{color}'
                group by t.trans_id,t.size,t.color,t.qid  
                """
                # print(sql)
                cursor.execute(sql)
                dispatch_defect_data_list = cursor.fetchone()
                # print(dispatch_defect_data_list)
                total_count_list = dispatch_defect_data_list[5]
                               
                sql = f"""  select sum(qty) total_count from defect_transaction_entry_mt where trans_id = '{trans_id}' 
                and defect_type = '{defect_type}' and trans_type ='dispatch'  """
                # print(sql)
                cursor.execute(sql)
                dispatch_defect_data = cursor.fetchone()
                total_count_all = dispatch_defect_data[0]
                
                cursor.close()
                
                return_arr = { "total_count_list" : total_count_list , "total_count_qid" : total_count_qid,"total_count_all" : total_count_all, "total_count" : total_count, "defect_type": defect_type}

                return JsonResponse(return_arr,safe=False) 

        elif flag == 'save_other_qty': 
            booking_list     = request.GET.getlist('booking_id')
            size_list     = request.GET.getlist('size')
            color_list    = request.GET.getlist('color')
            balance_cut_qty_list    = request.GET.getlist('balance_cut_qty')
            quantity_list = request.GET.getlist('cut_qty')
            tra_id_list = request.GET.getlist('tra_id')
            total_qty =0
            size_breakup =''
            return_arr = []
            curr_date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for booking_id,size, color,balance_cut_qty, quantity , tra_id in zip(booking_list,size_list, color_list,balance_cut_qty_list, quantity_list , tra_id_list):
                bid  = booking_id
                booking_id = SampleBookingMt.objects.get(id=booking_id)
                cursor =  connections['default'].cursor()
                sql = f""" 
                select s.id,s1.quantity as sample_qty,isnull(sum(c.qty),0) as cut_qty,isnull(( s1.quantity - isnull(sum(c.qty),0) ),0) balance_qty 
                from (select id,total_qty from sample_booking_mt ) s 
                join sample_size_quantity s1 on s.id  = s1.booking_id_id
                left join other_entry_dt c on s1.booking_id_id = c.booking_id and s1.size= c.size and s1.color = c.color
                where s.id ={bid} and s1.size='{size}' and s1.color ='{color}'
                group by s.id,s1.quantity               
                """
                cursor.execute(sql)
                cut_mt_data = cursor.fetchone()
                print(cut_mt_data)
                cursor.close()
                # int(cut_mt_data['balance_qty'])
                if size and color and int(quantity) > 0 and cut_mt_data[3] >= int(quantity):
                    total_qty = total_qty + int(quantity)
                    size_breakup =  size + ',' + size_breakup 
                    cursor =  connections['default'].cursor()
                    
                    if int(tra_id) > 0 :
                        sql = f""" 
                        update transaction_entry_mt set qty = {quantity},updated_by={curr_user} where booking_id ='{bid}' and size='{size}' and color ='{color}' and trans_type ='other' and id='{tra_id}'
                        """ 
                    else :    
                        sql = f""" 
                        insert into transaction_entry_mt (qty,size,is_active,updated_at,created_at,booking_no,booking_id,color,trans_type,created_by) 
                        values('{quantity}','{size}',1,'{curr_date_time}','{curr_date_time}','{booking_id}',{bid},'{color}','other','{curr_user}')                
                        """
                    # print(sql)
                    cursor.execute(sql)
                    cursor.close()
                    size_breakup =  size_breakup.rstrip(',')
            return_arr = {"total_qty" : total_qty, "size_breakup": size_breakup}

            return JsonResponse(return_arr,safe=False)   


        return HttpResponse('Data Not Saved')    

            