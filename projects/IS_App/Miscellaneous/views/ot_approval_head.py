from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster
from IS_Nexus.database import get_unit_list,get_ot_head_pending_list,get_dep_list,get_desg_list,get_ot_head_approve_list,get_ot_head_reject_list
from django.db import connections
from django.contrib import messages
# from Miscellaneous.models import OtApproval
from App_db.models import OtApproval
from datetime import datetime , timedelta

class OtApproval_head(View):
    def get(self,request):
        unit_code = request.GET.get('unit_code')
        dayno = request.GET.get('dayno')
        department = request.GET.get('dept')
        designation = request.GET.get('desg')
        ot_hour = request.GET.get('ot_hour')
        unit_list = LocationMaster.objects.filter(is_active=True)

        context = {
            'unit_code' :unit_code,
            'dayno' :dayno,
            'ot_hour' :ot_hour,
            'ot_hour_list' : range(1,13),
            'unit_list' : unit_list,
            'dept_list' : get_dep_list(),
            'desg_list' : get_desg_list(),
            'ot_emp_list' : get_ot_head_pending_list(dayno, department, designation, unit_code),
            'ot_emp_app_list' : get_ot_head_approve_list(dayno,department,designation,unit_code),
            'ot_emp_rej_list' : get_ot_head_reject_list(dayno,department,designation,unit_code)
            # 'ot_emp_temp_list' : ot_emp_temp_list(dayno,department,designation,unit_code,user=1)
        }
        return render(request,'ot_approval_head.html',context)
    
    def post(self, request):
        flag = request.POST.get('flag')
        is_saved = False
        def add_post():
            pass
        
        def other_post(flag_val):
            counter = request.POST.get('counter')
            now = datetime.now()
            curr_date = now.strftime("%Y-%m-%d %H:%M:%S")

            if counter:
                counter = int(counter) + 1

                for i in range(counter):
                    app_id = request.POST.get(f"app_id[{i}]")
                    app_check = request.POST.get(f"app_check[{i}]")

                    if flag_val==2 and app_check:
                        try:
                            cursor = connections['default'].cursor()
                            sql = f"""update ot_approval set approve_status={flag_val},approve_by=1,approve_date='{ curr_date }' where id='{app_id}' """
                            cursor.execute(sql)
                            is_saved = True
                        except:
                            messages.error(request,'Updation Invalid data') 

                    elif flag_val==3 and app_check:
                        try:
                            cursor = connections['default'].cursor()
                            sql = f"""update ot_approval set approve_status={flag_val},approve_by=1,approve_date='{ curr_date }' where id='{app_id}' """
                            cursor.execute(sql)
                            is_saved = True
                        except:
                            messages.error(request,'Updation Invalid data') 
            if is_saved:
                messages.success(request,'Data saved Success')

        flag = request.POST.get("flag")

        if flag == 'approve':
            other_post(2)
        elif flag == 'reject':
            other_post(3)
        else:
            add_post()

        return redirect('ot_approve_head_page') 
