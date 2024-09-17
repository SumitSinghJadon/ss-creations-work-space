from django.views import View
from django.shortcuts import redirect, render
# from Miscellaneous.models import ManpowerHrMt
from App_db.models import ManpowerHrMt, MmrMT
from IntelliSync_db.models import LocationMaster 
from IS_Nexus.database import (
    get_dep_list, get_desg_list, 
    get_dept_desg_hr_list, 
    get_dept_desg_hr_summ, 
    get_manpower_plan_data,
    get_unit_list,
    get_present_tailor
)
from django.contrib import messages
from django.db import connections
from datetime import datetime , timedelta


class ManpowerPlanning_hr(View):
    def get(self, request):
        curr_date = datetime.today().strftime('%Y-%m-%d')
        unit_list = LocationMaster.objects.filter(is_active=True)
        mmr_list = MmrMT.objects.filter(is_active=True,from_date__lte=curr_date,to_date__gte=curr_date)

        dayno = request.GET.get('dayno')
        unit_code = request.GET.get('unit_code')
        mmr_code = request.GET.get('mmr_code')
        payroll_tailor_list = get_present_tailor(dayno,unit_code)
        plan_mmr =''
        actual_mmr=''
        present_tailor=0

        if payroll_tailor_list:
            present_tailor = payroll_tailor_list[0]['tailor']
            total_onroll = payroll_tailor_list[0]['total_onroll']
            total_present = payroll_tailor_list[0]['total_present']
            total_approve = payroll_tailor_list[0]['total_approve']
            if present_tailor !=0:
                plan_mmr = round((total_approve / present_tailor) * 100,2)
                actual_mmr = round((total_present / present_tailor) * 100,2) 

        
        # print(plan_mmr)
        context = {
            'dept_desg_summ_list' : get_dept_desg_hr_summ(dayno,unit_code),
            'dept_desg_list' : get_dept_desg_hr_list(dayno,mmr_code,unit_code),
            'present_tailor' : present_tailor,
            'unit_list' : unit_list,
            'plan_mmr' : plan_mmr,
            'actual_mmr' : actual_mmr,
            'mmr_list' : mmr_list,
            'mmr_code' : mmr_code,
            'dept_list' : get_dep_list(),
            'desg_list' : get_desg_list(),
            'curr_date' : curr_date
        }
        return render(request, 'manpower_hr.html', context)

    def post(self, request):
        dayno = request.POST.get('dayno')
        unit_code = request.POST.get('unit_code')
        mmr_code = request.POST.get('mmr_code') 

        # def add_post():
            # dept_sing = request.POST.get("dept_sing")
            # desg_sing = request.POST.get("desg_sing")
            # manp_sing = request.POST.get("manp_sing")
            # print('\n\n', dept_sing, dept_sing,unit_code, '\n\n')
            # ManpowerHrMt.objects.create(
                # department=dept_sing,designation=desg_sing,manpower=manp_sing,unit_code=unit_code
            # )
        
        def other_post():
            dayno = request.POST.get('dayno')
            mmr_code = request.POST.get("mmr_code")
            counter = request.POST.get('counter')

            if counter:
                counter = int(counter) + 1
                for i in range(counter):
                    dept = request.POST.get(f"dept_code[{i}]")
                    desg = request.POST.get(f"desg_code[{i}]")
                    onroll = request.POST.get(f"onroll[{i}]")
                    app_manp = request.POST.get(f"app_manp[{i}]")
                    remarks = request.POST.get(f"remarks[{i}]")
                    app_id = request.POST.get(f"app_id[{i}]")

                    if dept and desg and onroll and app_manp and app_id=='0':
                        try:
                            ManpowerHrMt.objects.create(
                                mmr_code = mmr_code, department=dept, designation=desg, onroll=onroll, manpower=app_manp, unit_code=unit_code, remarks=remarks, dayno=dayno
                            )
                            messages.success(request,'Data saved Success')

                        except Exception as e:
                            print(e)
                            messages.error(request,'Insertion Invalid data')

                    elif dept and desg and onroll and app_manp:
                        try:
                            cursor = connections['default'].cursor()
                            sql = f"""update manpower_hr set remarks='{remarks}' where id='{app_id}' """
                            cursor.execute(sql)
                            # messages.success(request,'Data saved Success')
                        except:
                            messages.error(request,'Updation Invalid data') 

        flag = request.POST.get("flag")
        if flag == 'add_btn':
            # add_post()
            pass
        else:
            other_post()

        return redirect(f'/miscellaneous/manpower_hr/?unit_code={unit_code}&mmr_code={mmr_code}')


# from django.shortcuts import render,redirect
# from django.views import View
# from django.http import HttpResponse
# from Miscellaneous.models import ManpowerHrMt
# from django.contrib import messages
# from SharedApp.database import get_dep_list,get_desg_list,get_dept_desg_list,get_manpower_plan_data,get_unit_list
# from django.db import connections


# class ManpowerPlanning(View):

#     def get(self,request):
#         #return HttpResponse("hello")
#         #print(ManpowerHrMt.objects.all())
       
#         #dept_list  = [{'1':'Cutting'},{'2':'Stitching'},{'3':'FInishing'}]
#         # plan_manp = get_manpower_plan_data('200','300',1)
#         # print(plan_manp)
#         unit_code = request.GET.get('unit_code')
#         context = {
#             'dept_desg_list' : get_dept_desg_list(),
#             'unit_list' : get_unit_list(),
#             'dept_list' : get_dep_list(),
#             'desg_list' : get_desg_list()
#         }
#         return render(request,"manpower_planning.html",context)

