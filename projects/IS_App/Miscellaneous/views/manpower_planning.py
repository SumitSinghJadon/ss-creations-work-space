from django.views import View
from django.shortcuts import redirect, render
from IntelliSync_db.models import LocationMaster
from IS_Nexus.database import get_dep_list,get_desg_list,get_dept_desg_list,get_manpower_plan_data,get_unit_list
from django.contrib import messages
from django.db import connections
from App_db.models import MmrMT, ManpowerplanMT 
# from Miscellaneous.models import MmrMT, ManpowerplanMT 
from datetime import datetime , timedelta


class ManpowerPlanning(View):
    def get(self, request):
        curr_date = datetime.today().strftime('%Y-%m-%d')
        unit_list = LocationMaster.objects.filter(is_active=True)
        mmr_list = MmrMT.objects.filter(is_active=True,from_date__lte=curr_date,to_date__gte=curr_date)
        unit_code = request.GET.get('unit_code')
        mmr_code = request.GET.get('mmr_code')
        context = {
            'dept_desg_list' : get_dept_desg_list(curr_date,mmr_code,unit_code),
            'unit_list' : unit_list,
            'mmr_list' : mmr_list,
            'mmr_code' : mmr_code,
            'dept_list' : get_dep_list(),
            'desg_list' : get_desg_list()
        }
        return render(request, 'manpower_planning.html', context)


    def post(self, request):
        unit_code = request.POST.get('unit_code')
        mmr_code = request.POST.get('mmr_code') 

        def add_post():
            dept_sing = request.POST.get("dept_sing")
            desg_sing = request.POST.get("desg_sing")
            manp_sing = request.POST.get("manp_sing")
            
            ManpowerplanMT.objects.create(
                department=dept_sing,designation=desg_sing,manpower=manp_sing,unit_code=unit_code
            )
        
        def other_post():
            counter = request.POST.get('counter')
            if counter:
                counter = int(counter) + 1
                for i in range(counter):
                    dept = request.POST.get(f"dept_code[{i}]")
                    desg = request.POST.get(f"desg_code[{i}]")
                    manp = request.POST.get(f"manp[{i}]")
                    app_id = request.POST.get(f"app_id[{i}]")
                    
                    plan_manp = get_manpower_plan_data(dept,desg,1)
                    #lengh = len(plan_manp)
                    #print(dept,desg,manp,plan_manp )
                    if dept and desg and manp and not plan_manp:
                        try:
                            ManpowerplanMT.objects.create(
                                mmr_code=mmr_code,department=dept,designation=desg,manpower=manp,unit_code=unit_code
                            )
                            # messages.success(request,'Data saved Success')
                        except:
                            messages.error(request,'Insertion Invalid data')
                    elif dept and desg and manp and plan_manp:
                        try:
                            cursor = connections['default'].cursor()
                            sql = f"""update manpower_plan set manpower='{manp}' where id='{app_id}' """
                            cursor.execute(sql)
                            # messages.success(request,'Data saved Success')
                        except:
                            messages.error(request,'Updation Invalid data') 

        flag = request.POST.get("flag")
        if flag == 'add_btn':
            add_post()

        else:
            other_post()

        return redirect(f'/miscellaneous/manpower/?unit_code={unit_code}&mmr_code={mmr_code}')


# from django.shortcuts import render,redirect
# from django.views import View
# from django.http import HttpResponse
# from Miscellaneous.models import ManpowerplanMT
# from django.contrib import messages
# from SharedApp.database import get_dep_list,get_desg_list,get_dept_desg_list,get_manpower_plan_data,get_unit_list
# from django.db import connections


# class ManpowerPlanning(View):

#     def get(self,request):
#         #return HttpResponse("hello")
#         #print(ManpowerplanMT.objects.all())
       
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

