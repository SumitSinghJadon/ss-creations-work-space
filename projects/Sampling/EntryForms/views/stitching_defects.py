from django.views import View
from django.shortcuts import render
from IntelliSync_db.models import CommonMaster, FirstLevelMaster , SecondLevelMaster
from functions import delete_unused_stitch_temp_defect_trans , get_trans_srno_data , get_trans_srno_data_disp
from django.contrib import messages
from django.db import connection,connections
from datetime import datetime , timedelta


class StitchingDefectsView(View):
    def get(self, request):
        trans_id = request.GET.get('trans_id')
        delete_unused_stitch_temp_defect_trans(trans_id)
        trans_srno_list = get_trans_srno_data(trans_id,'stitch')
        trans_srno_list_disp = get_trans_srno_data_disp(trans_id,'stitch')
        
        defect_list = FirstLevelMaster.objects.filter(is_active=True, common_master__name='Stitching', common_master_type__code = 'CT-16').using('intellisync_db')
        # for item in defect_list:
        #     print('\n\n', item.master_type.code, '\n\n')
        
        context ={
            'defect_list' : defect_list,
            'trans_srno_list' : trans_srno_list,
            'trans_srno_list_disp' : trans_srno_list_disp
        }
        return render(request, 'stitching_defects.html',context)
    

    def post(self, request):
        trans_id = request.GET.get('trans_id')
        
        try:
            counter = request.POST.get('counter')
            if counter:
                counter = int(counter) + 1
                for i in range(counter):
                    size = request.POST.get(f"size[{i}]")
                    color = request.POST.get(f"color[{i}]")
                    qid = request.POST.get(f"qid[{i}]")
                    qty = request.POST.get(f"qty[{i}]")
                    defect = request.POST.get(f"defect[{i}]")
                    defect_count = request.POST.get(f"defect_count[{i}]")
                    result = request.POST.get(f"result[{i}]")
                    curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    #lengh = len(plan_manp)
                    # print(unit_code,dayno,emp_code,name,ot_hour_val )

                    if result:
                        try:
                            cursor = connections['default'].cursor()
                            # print(is_data)
                            if result:
                                sql_ins_size  = f"""
                                insert into stitch_entry_size_dt(trans_id,qty,size,qid,color,result,defect_count,defect,is_active,updated_at,created_at) 
                                values('{trans_id}','{qty}','{size}','{qid}','{color}','{result}','{defect_count}','{defect}',1,'{curr_date}','{curr_date}')
                                """
                                cursor.execute(sql_ins_size)
                                cursor.close()
                                messages.success(request,'Data saved Success')
                            else:
                                messages.warning(request,'Already exists.')
                                
                        except Exception as e:
                            print(e)
                            messages.error(request,'Insertion Invalid data')

            
            cursor =  connections['default'].cursor()
            sql_ins = f""" insert into defect_stitch_entry_dt(qty,is_active,updated_at,created_at,defect_type,trans_type,defect_id,trans_id,size,qid,color) 
            (select qty,is_active,updated_at,created_at,defect_type,trans_type,defect_id,trans_id,size,qid,color
            from defect_transaction_entry_mt where trans_id = {trans_id} and trans_type='stitch' )  """
            # print(sql_ins)
            cursor.execute(sql_ins)
            cursor.close()
            
            cursor =  connections['default'].cursor()
            sql_del = f""" delete from defect_transaction_entry_mt where trans_id = {trans_id} and trans_type='stitch' """
            cursor.execute(sql_del)
            cursor.close()
                    
            messages.success(request, "Success! The entry has been created.")

        except Exception as e:
            print(e)    
            messages.error(request, "Data Not Saved")

        trans_srno_list = get_trans_srno_data(trans_id,'stitch')
        trans_srno_list_disp = get_trans_srno_data_disp(trans_id,'stitch')
        defect_list = FirstLevelMaster.objects.filter(is_active=True, common_master__name='Stitching', common_master_type__code = 'CT-16').using('intellisync_db')
        context ={
            'defect_list' : defect_list,
            'trans_srno_list' : trans_srno_list,
            'trans_srno_list_disp' : trans_srno_list_disp
        }
        return render(request, 'stitching_defects.html',context)