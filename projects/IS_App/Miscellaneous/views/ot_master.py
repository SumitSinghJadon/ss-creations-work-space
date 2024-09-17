from django.views import View
from django.shortcuts import redirect, render
from App_db.models import OTMT
from IntelliSync_db.models import LocationMaster
from IS_Nexus.database import get_ot_master_list,get_unit_list,get_dep_list,get_unit_dept_list
from django.contrib import messages
from django.db import connections
from django.http import HttpResponse
from datetime import datetime , timedelta

class Ot_Master_add(View):
    def get(self, request):
        now = datetime.now() # current date and time
        today_date = now.strftime("%Y-%m-%d")
        unit_list = LocationMaster.objects.filter(is_active=True)
        unit_code = request.GET.get('unit_code')
        # print(unit_code,today_date)
        context = {
            'ot_master_list' : get_unit_dept_list(today_date,unit_code),
            'dept_list' : get_dep_list(),
            'unit_list' : unit_list
        }
        return render(request, 'ot_master.html', context)


    def post(self, request):
        # print('hello 1')
        unit_code = request.GET.get('unit_code')

        def add_ot_master():
            counter = request.POST.get('counter')
            if counter:
                counter = int(counter) + 1
                for i in range(counter):
                    dep_code = request.POST.get(f"dep_code[{i}]")
                    ot_month = request.POST.get(f"ot_month[{i}]")
                    ot_daily = request.POST.get(f"ot_daily[{i}]")
                    app_id = request.POST.get(f"app_id[{i}]")
                                
                    #lengh = len(plan_manp)
                    #print(unit_code,dep_code,ot_month,ot_daily,app_id )

                    if dep_code and ot_month and ot_daily and not app_id:
                        try:
                            cursor = connections['default'].cursor()
                            is_data = OTMT.objects.filter(unit_code = unit_code, dep_code = dep_code)
                            # print(is_data)
                            if not is_data.exists():
                                OTMT.objects.create(
                                    unit_code=unit_code,
                                    dep_code=dep_code,
                                    ot_month=ot_month,
                                    ot_daily=ot_daily
                                )
                                messages.success(request,'Data saved Success')
                            else:
                                messages.warning(request,'Already exists.')
                                
                        except:
                            messages.error(request,'Insertion Invalid data')
                    elif dep_code and ot_month and ot_daily and app_id:
                        # print(unit_code,dep_code)
                        try:
                            OTMT.objects.filter(id=app_id).update(
                                ot_month=ot_month,
                                ot_daily=ot_daily
                            )
                        except:
                            messages.error(request,'Updation Invalid data') 
                                         

        flag = request.POST.get("flag")
        if flag == 'add_btn':
            # print('hello 4')
            f=1
        else:
            add_ot_master()

        return redirect(f'/miscellaneous/ot_master')



