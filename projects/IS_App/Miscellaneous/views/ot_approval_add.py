from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster
from IS_Nexus.database import get_unit_list,get_ot_emp_list,get_dep_list,get_desg_list
from django.db import connections
from django.contrib import messages
# from Miscellaneous.models import OtApproval
from App_db.models import OtApproval
from datetime import datetime , timedelta


class OtApproval_view(View):
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
            'ot_emp_list' : get_ot_emp_list(dayno,department,designation,unit_code),
        }
        return render(request,'ot_approval_add.html',context)
    
    def post(self, request):
        unit_code = request.POST.get('unit_code')
        dayno = request.POST.get('dayno')
        curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        def add_post():
            pass
        
        def other_post():
            counter = request.POST.get('counter')
            is_saved = False
            if counter:
                counter = int(counter) + 1
                for i in range(counter):
                    emp_code = request.POST.get(f"emp_code[{i}]")
                    name = request.POST.get(f"name[{i}]")
                    ot_hour_val = request.POST.get(f"ot_hour2[{i}]")
                    app_id = request.POST.get(f"app_id[{i}]")

                    if emp_code and ot_hour_val:
                        try:
                            app_chk_data = OtApproval.objects.filter(dayno = dayno, emp_code = emp_code,approve_status=1)
                            is_data = OtApproval.objects.filter(dayno = dayno, emp_code = emp_code)

                            if not is_data.exists():
                                OtApproval.objects.create(
                                    unit_code = unit_code,
                                    dayno = dayno,
                                    emp_code = emp_code,
                                    name = name,
                                    ot_hour = ot_hour_val,
                                    approve_status = 1
                                )
                                is_saved = True
                            else:
                                messages.warning(request,'Already exists.')
                                
                        except Exception as e:
                            print(e)
                            messages.error(request,'Insertion Invalid data')

                    elif emp_code and ot_hour_val and app_id and app_chk_data:
                        try:
                            cursor = connections['default'].cursor()
                            # sql = f"""update ot_approval set ot_hour=None where id='{app_id}' """
                            # cursor.execute(sql)
                            # messages.success(request,'Data saved Success')
                        except:
                            messages.error(request,'Updation Invalid data') 

            if is_saved:
                messages.success(request,'Data saved Success')
                
        flag = request.POST.get("flag")
        
        if flag == 'add_btn':
            add_post()

        else:
            other_post()

        return redirect(f'/miscellaneous/ot_add/?unit_code={unit_code}&dayno={dayno}')
