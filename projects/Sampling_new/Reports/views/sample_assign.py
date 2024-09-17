from django.views import View
from django.shortcuts import render , redirect
from IntelliSync_db.models import CommonMaster, FirstLevelMaster , SecondLevelMaster
from functions import delete_unused_stitch_temp_defect_trans , get_trans_srno_data , get_trans_srno_data_disp
from django.contrib import messages
from django.db import connection,connections
from datetime import datetime , timedelta
from IS_Nexus.functions.shortcuts import get_next_number,pay_db

class SampleAssignView(View):
    def get(self, request):
        booking_id = request.GET.get('booking_id')
        hold_reason_list = CommonMaster.objects.filter(master_type__code='CT-38', is_active=True).values('id','name').order_by('name')
        # hold_reason_list = CommonMaster.objects.filter(master_type__code='CT-38', is_active=True).using('intellisync_db')
        
        if request.GET.get('from_date') and request.GET.get('to_date'):
            from_date = request.GET.get('from_date')
            to_date = request.GET.get('to_date')
        else:
             from_date = datetime.today().strftime('%Y-%m-01')
             to_date = datetime.today().strftime('%Y-%m-%d')
        
        if request.GET.get('buyer'):
            buyer = request.GET.get('buyer')
        else:
            buyer = None
            
        if request.GET.get('style'):
            style = request.GET.get('style')
        else:
            style = None
            
        data_list =[]
        if from_date and to_date:
            cursor =  connections['default'].cursor()
            
            sql_cutter1 = f""" EXEC GET_SAMP_REPORTS 'sample_assign','{from_date}','{to_date}', """
            
            if request.GET.get('buyer'):
                buyer = request.GET.get('buyer')
                sql_cutter2 = f""" '{buyer}', """
            else:
                sql_cutter2 = f""" NULL, """
            
            if request.GET.get('closer') == 'C':
                sql_cutter3 = f""" 'close' """
            else:
                sql_cutter3 = f""" NULL """
                
            sql_cutter = sql_cutter1 + sql_cutter2 + sql_cutter3
            # print(sql_cutter)
            cursor.execute(sql_cutter)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        # print(data_list)
        curr_date = datetime.today().strftime('%Y-%m-%d')
        db_name = pay_db(curr_date)
        
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
        samp_dept_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        cursor.close()

        cursor =  connections['default'].cursor()
        sql_cutter = f""" select buyer_code,buyer_name from sample_booking_mt (nolock) group by buyer_code,buyer_name order by buyer_name asc """
        cursor.execute(sql_cutter)
        samp_buyer =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
        
        context ={
            'booking_id' : booking_id,
            'hold_reason_list' : hold_reason_list,
            'data_list' : data_list,
            'samp_dept_list' : samp_dept_list,
            'samp_buyer' : samp_buyer,
            'from_date' : from_date,
            'to_date' : to_date,
            'buyer' : buyer,
            'style' : style,
        }
        return render(request, 'sample_assign.html',context)
    
    def post(self, request):
        curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        def add_post():
            pass
        
        def other_post():
            counter = request.POST.get('counter')
            if counter:
                counter = int(counter) + 1
                for i in range(counter):
                    status = request.POST.get(f"status[{i}]")
                    booking_id = request.POST.get(f"booking_id[{i}]")

                    if status and booking_id:

                        closer_status = request.POST.get(f"closer_status[{i}]")
                        sample_dept = request.POST.get(f"sample_dept[{i}]")
                        cut_assign_date = request.POST.get(f"cut_assign_date[{i}]")
                        stitch_assign_date = request.POST.get(f"stitch_assign_date[{i}]")
                        finish_assign_date = request.POST.get(f"finish_assign_date[{i}]")
                        dispatch_assign_date = request.POST.get(f"dispatch_assign_date[{i}]")

                        hold_process_val = request.POST.get(f"hold_process[{i}]")
                       
                        cassign_date_chk = cut_assign_date 
                        if cut_assign_date:
                            cassign_date_chk = cassign_date_chk.replace("T", " ")
                        else:
                            cassign_date_chk =''
                        
                        sassign_date_chk = stitch_assign_date 
                        if stitch_assign_date:
                            sassign_date_chk = sassign_date_chk.replace("T", " ")
                        else:
                            sassign_date_chk =''

                        fassign_date_chk = finish_assign_date 
                        if finish_assign_date:
                            fassign_date_chk = fassign_date_chk.replace("T", " ")
                        else:
                            fassign_date_chk =''

                        dassign_date_chk = dispatch_assign_date 
                        if dispatch_assign_date:
                            dassign_date_chk = dassign_date_chk.replace("T", " ")
                        else:
                            dassign_date_chk =''

                        # if sassign_date <= cassign_date:
                        #     print('wrong date')
                        # else:
                        #     print('okk')
                        # print(status,booking_id,'ccc--',cassign_date_chk,'sss--',sassign_date_chk,'ffff--',fassign_date_chk,'dddd---',dassign_date_chk)
                        # print(status,booking_id,stitch_assign_date,'sss--',sassign_date_chk,'ccc--',cassign_date_chk)
                        if hold_process_val:
                            hold_action_val = request.POST.get(f"hold_action[{i}]")
                            hold_reason_val = request.POST.get(f"hold_reason[{i}]")
                            hold_remarks_val = request.POST.get(f"hold_process[{i}]")
                            try:
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update sample_booking_mt set 
                                trans_hold_process='{hold_process_val}' ,
                                trans_hold_reason='{hold_reason_val}' ,
                                trans_hold_remarks='{hold_remarks_val}' 
                                where id ='{booking_id}' """
                                cursor.execute(sql_del)

                                if hold_action_val == '0':
                                    sql_cut_unhold = f""" update cutting_entry_mt set sample_status ='O' where booking_id ='{booking_id}' and sample_status ='H' """
                                    cursor.execute(sql_cut_unhold)
                                    sql_stitch_unhold = f""" update stitch_entry_mt set stitch_status ='O' where booking_id ='{booking_id}'  and stitch_status ='H' """
                                    cursor.execute(sql_stitch_unhold)
                                    sql_finish_unhold = f""" update finish_entry_mt set qa_status ='O' where booking_id ='{booking_id}'  and qa_status ='H' """
                                    cursor.execute(sql_finish_unhold)

                                cursor.close()
                                
                            except Exception as e:
                                print(e)
                                messages.error(request,'Hold Process Not Updated')

                        if status and booking_id and closer_status == 'close':
                            try:
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update sample_booking_mt set is_active='0' where id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                                
                            except Exception as e:
                                print(e)
                                messages.error(request,'Cutting Assign Date Not Updated')

                        if status and booking_id and sample_dept:
                            try:
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update sample_booking_mt set dep_code='{sample_dept}' where id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                                
                            except Exception as e:
                                print(e)
                                messages.error(request,'Cutting Assign Date Not Updated')

                        if status and booking_id and cut_assign_date:
                            try:
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update sample_booking_mt set cut_assign_date='{cut_assign_date}' where id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                                
                                cursor = connections['default'].cursor()
                                sql_del = f""" update cutting_entry_mt set assign_date='{cut_assign_date}' where booking_id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                            except Exception as e:
                                print(e)
                                messages.error(request,'Cutting Assign Date Not Updated')
                        if status and booking_id and stitch_assign_date and sassign_date_chk > cassign_date_chk:
                            try:
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update sample_booking_mt set stitch_assign_date='{stitch_assign_date}' where id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                                
                                cursor = connections['default'].cursor()
                                sql_del = f""" update stitch_entry_mt set assign_date='{stitch_assign_date}' where booking_id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                            except Exception as e:
                                print(e)
                                messages.error(request,'Stitch Assign Date Not Updated')
                        if status and booking_id and finish_assign_date and fassign_date_chk > sassign_date_chk:
                            try:
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update sample_booking_mt set finish_assign_date='{finish_assign_date}' where id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                                
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update finish_entry_mt set assign_date='{finish_assign_date}' where booking_id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                            except Exception as e:
                                print(e)
                                messages.error(request,'Finish Assign Date Not Updated')
                        if status and booking_id and dispatch_assign_date and dassign_date_chk > fassign_date_chk:
                            try:
                                cursor = connections['default'].cursor()
                                sql_del = f"""  update sample_booking_mt set dispatch_assign_date='{dispatch_assign_date}' where id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                                
                                cursor = connections['default'].cursor()
                                sql_del = f""" update dispatch_entry_mt set assign_date='{dispatch_assign_date}' where booking_id ='{booking_id}' """
                                cursor.execute(sql_del)
                                cursor.close()
                            except Exception as e:
                                print(e)
                                messages.error(request,'Dispatch Assign Date Not Updated')

        flag = request.POST.get("flag")
        if flag == 'add_btn':
            add_post()

        else:
            other_post()

        return redirect(f'/entry-forms/sample-assign/')
    