from django.views import View
from django.shortcuts import redirect, render
# from Miscellaneous.models import MmrMT
from App_db.models import MmrMT
from IntelliSync_db.models import LocationMaster
from IS_Nexus.database import get_mmr_list,get_unit_list
from django.contrib import messages
from django.db import connections
from django.http import HttpResponse
from datetime import datetime , timedelta

class Mmr(View):
    def get(self, request):
        unit_list = LocationMaster.objects.filter(is_active=True)
        #print(unit_list)
        unit_code = request.GET.get('unit_code')
        context = {
            'mmr_list' : get_mmr_list(unit_code),
            'unit_list' : unit_list
        }
        return render(request, 'mmr.html', context)


    def post(self, request):
        # print('hello 1')
        unit_code = request.GET.get('unit_code')
        def other_post():
            # print('hello 2')
            counter = 1
            if counter:
                counter = int(counter) + 1
                for i in range(counter):
                    #unit_code = request.POST.get(f"unit_code[{i}]")
                    from_date = request.POST.get(f"from_date")
                    to_date = request.POST.get(f"to_date")
                    mmr_id = request.POST.get(f"id[{i}]",None)
                    #print('hello')
                    
                    #lengh = len(plan_manp)
                    #print(dept,desg,manp,plan_manp )
                    if mmr_id:
                            try:
                                cursor = connections['default'].cursor()
                                sql = f"""update mmr_mt set from_date='{from_date}',to_date='{to_date}' where id='{mmr_id}' """
                                cursor.execute(sql)
                            # messages.success(request,'Data saved Success')
                            except:
                                messages.error(request,'Updation Invalid data') 
                    else:
                        try:
                            a= MmrMT.objects.create(
                                from_date=from_date,
                                to_date=to_date,
                                unit_code=unit_code
                            )
                            print(a)
                            # messages.success(request,'Data saved Success')
                        except:
                            messages.error(request,'Insertion Invalid data')

        def add_mmr():
            # cursor = connections['default'].cursor()
            # sql = """ select max() from mmr_mt """
            max_no = MmrMT.objects.all().values("id").last()
            if not max_no:
                max_no =1
            else:
                max_no = int(max_no['id']) + 1
            prev_date = datetime.today().strftime('%d%m%y') 
            mmr_code = f"MMR/{prev_date}/{max_no}"
            unit_code = request.POST.get("unit_code")
            from_date = request.POST.get("from_date")
            to_date = request.POST.get("to_date")
            if unit_code and from_date and to_date:
                MmrMT.objects.create(
                    mmr_code=mmr_code,
                    unit_code=unit_code,
                    from_date=from_date,
                    to_date=to_date
                )
                messages.success(request,'Data saved')
            else:
                messages.error(request,'Invalid Data')
             

        flag = request.POST.get("flag")
        if flag == 'add_btn':
            print('hello 4')
            f=1
        else:
            add_mmr()

        return redirect(f'/miscellaneous/mmr')



