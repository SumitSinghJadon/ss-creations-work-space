from django.views import View
from django.shortcuts import render
from IS_Nexus.functions import execute_sql
from IS_Nexus.database.is_hrms import get_payroll_db_name
from Payroll_db.models import EmployeeMaster
from django.db.models import F
from datetime import datetime
from IntelliSync_db.models import UserPermissionMaster, LocationPermission, User, LocationMaster
from Payroll_db.models import EmployeeMaster


class Dashboard(View):
    def get(self, request):
        # hr_mail = LocationPermission.objects.filter(
        #     location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode='HO00043').loc_code), 
        #     user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
        # ).values_list('user__email').exclude(user__email=None)

        def time_to_float(time_str):
            if time_str.strip():
                hours, minutes = map(int, time_str.split(':'))
                return round(hours + minutes / 60, 2)
            else:
                return 0
        
        sql = """
            select emp_dob, emp_paycode, emp_name, dep.dep_name, loc.loc_name, des.des_name
            from tbemp emp
            join tbdep dep on emp.dep_code = dep.dep_code
            join tblocation loc on emp.loc_code = loc.loc_code
            join tbdes des on emp.des_code = des.des_code
            WHERE resign=0 and MONTH(emp_dob) = MONTH(GETDATE()) AND DAY(emp_dob) = DAY(GETDATE())
        """
        dob_data = execute_sql(get_payroll_db_name(datetime.now()), sql)

        sql = """
            select emp_paycode, emp_name, dep.dep_name, loc.loc_name, des.des_name, emp.emp_doj
            from tbemp emp
            join tbdep dep on emp.dep_code = dep.dep_code
            join tblocation loc on emp.loc_code = loc.loc_code
            join tbdes des on emp.des_code = des.des_code
            WHERE CONVERT(date, emp.emp_doj) = CONVERT(date, GETDATE())
        """
        doj_data = execute_sql(get_payroll_db_name(datetime.now()), sql)

        user = request.user

        current_month = datetime.now().month if datetime.now().month < 4 else datetime.now().month+12

        # Data fro Dashboard Graph

        in_time_list=EmployeeMaster.objects.filter(
            time_master_emp_code__month_no=1
        ).values_list(
            *[f'time_master_emp_code__idt{i}' for i in range(1, 32)]
        ).order_by('emp_code').filter(emp_paycode='HO00043').using(get_payroll_db_name(datetime.now()))
        in_time_list = [time_to_float(value) for value in in_time_list[0]]

        out_time_list=EmployeeMaster.objects.filter(
            time_master_emp_code__month_no=1
        ).values_list(
            *[f'time_master_emp_code__odt{i}' for i in range(1, 32)]
        ).order_by('emp_code').filter(emp_paycode='HO00043').using(get_payroll_db_name(datetime.now()))
        out_time_list = [time_to_float(value) for value in out_time_list[0]]

        working_hour_list=EmployeeMaster.objects.filter(
            time_hour_day_emp_code__month_no=1
        ).values_list(
            *[f'time_hour_day_emp_code__thr{i}' for i in range(1, 32)]
        ).order_by('emp_code').filter(emp_paycode='HO00043').using(get_payroll_db_name(datetime.now()))
        working_hour_list = [time_to_float(value) for value in working_hour_list[0]]

        chart_data = {
            "in_time_list" : in_time_list,
            "out_time_list" : out_time_list,
            "working_hour_list" : working_hour_list,
        }

        context = {
            'dob_list' : dob_data,
            'doj_list' : doj_data,
            'chart_data' : chart_data
        }

        return render(request, 'dashboard.html', context)


