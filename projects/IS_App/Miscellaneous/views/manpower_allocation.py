from django.views import View
from django.shortcuts import redirect,render
from IntelliSync_db.models import LocationMaster
from IS_Nexus.database import get_unit_list,get_ot_emp_list,get_dep_list,get_desg_list
from django.db import connections
from django.contrib import messages
# from Miscellaneous.models import OtApproval
from App_db.models import OtApproval
from datetime import datetime , timedelta


class ManpowerAllocationView(View):
    def get(self,request):
        unit_code = request.GET.get('unit_code')
        if request.GET.get('dayno'):
            dayno = request.GET.get('dayno')
        else:
            dayno = datetime.today().strftime('%Y-%m-%d')

        unit_list = LocationMaster.objects.filter(is_active=True)
        data_list = []
        data_list2 = []
        if dayno and unit_code:
            cursor = connections['default'].cursor()
            sql = f""" 
                 EXEC [GET_MANPOWER_ALLOC] '{unit_code}','tailor','{dayno}'
            """
            # print(sql)
            cursor.execute(sql)
            data_list =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            cursor.close()

            # cursor = connections['default'].cursor()
            # sql = f""" 
            #      EXEC [GET_MANPOWER_ALLOC] '{unit_code}','manp_summ','{dayno}'
            # """
            # # print(sql)
            # cursor.execute(sql)
            # data_list2 =  [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in cursor.fetchall()]
            # cursor.close()
            # print(data_list2.keys)
        # print(data_list)
        line_type_list = [{ 'name' : 'MAIN' }]
        line_name_list = [{ 'name' : 'GF' },{ 'name' : 'FF' },{ 'name' : 'SF' } ]
        context = {
            'unit_code' :unit_code,
            'line_type_list' :line_type_list,
            'line_name_list' :line_name_list,
            'dayno' :dayno,
            'unit_list' : unit_list,
            'data_list' : data_list,
            'data_list2' : data_list2,
        }
        return render(request,'manpower_allocation.html',context)
    
    def post(self, request):
        unit_code = request.POST.get('unit_code')
        dayno = request.POST.get('dayno')
        curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        def add_post():
            pass
        
        def other_post():
            pass
                
        flag = request.POST.get("flag")
        
        if flag == 'add_btn':
            add_post()

        else:
            other_post()

        return redirect(f'/miscellaneous/alloc/?unit_code={unit_code}&dayno={dayno}')
