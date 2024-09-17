from django.views import View
from django.shortcuts import redirect, render
from IS_Nexus.database.is_hrms import getEmployeeDetails,getSundays,get_payroll_db_name, hrms_mailer
from datetime import datetime
from HRMS_db.models import LeaveApplication
from IntelliSync_db.models import LocationMaster ,LocationPermission ,UserPermissionMaster , CommonMaster
from Payroll_db.models import EmployeeMaster ,HolidayMaster
from datetime import datetime, timedelta
from IS_Nexus.functions import messages
from .params import date_parm
from django.template.loader import render_to_string

class CompOffView(View):
    
    def get(self,request):
        year_list=CommonMaster.objects.filter(master_type__code='CT-20').values('name','value').order_by('-name')
        month_list=CommonMaster.objects.filter(master_type__code='CT-19').values('name','value').order_by('value')
        current_year=datetime.now().year
        current_month=datetime.now().month
        employee = getEmployeeDetails(request.user.username)
        comoff_list = LeaveApplication.objects.filter(user=request.user,application_type='Comp-off')
        working_days=HolidayMaster.objects.filter(h_date__contains=f'{current_year}').values('h_name','h_date').distinct().using(get_payroll_db_name(datetime.now()))

        enabled_dates=getSundays()
        
        for item in working_days:
            if item["h_date"].replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
                enabled_dates.append(item["h_date"].strftime('%Y-%m-%d'))
        
        context = {
            'employee' : employee['data'],
            'min_date' : datetime.now()-timedelta(days=date_parm),
            'comoff_list' : comoff_list,
            'year_list' : year_list,
            'month_list' : month_list,
            'enabled_dates' : enabled_dates,
            'current_year' : current_year,
            'current_month' : current_month
        }
        return render(request,"compoffApplication.html",context)
    
    def post(self,request):
        if 'cancel_application' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Cancelled',cancelled_on=datetime.now())   
        else:
            from_date =request.POST.get("leave_from")
            till_date =request.POST.get("working_day")
            day_part = request.POST.get("day_part")
            address = request.POST.get("address")
            phone = request.POST.get("phone")
            reason = request.POST.get("reason")
            department=request.POST.get("department")
            applied_on = datetime.now()

            try:
                data=LeaveApplication.objects.create(
                    user = request.user,
                    dep = department,
                    application_type = 'Comp-off',
                    from_date = from_date,
                    till_date = till_date,
                    day_part = day_part,
                    reason = reason, 
                    address = address, 
                    mobile_number = phone,
                    status = 'Pending',
                    applied_on=applied_on 
                )

                hr_mail = LocationPermission.objects.filter(
                    location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode=request.user.username).loc_code), 
                    user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
                ).values_list('user__username','user__email').exclude(user__email=None)

                try:
                    hrms_mailer(f'Comp-off Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":request.user.reporting_manager.username}), [request.user.reporting_manager.email])

                    hrms_mailer(f'Comp-off Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":hr_mail[0][0]}), [hr_mail[0][1]])
                
                except Exception as e:
                    messages.error(request,"Unable to send email to your head of department")
                
                
            except Exception as e:
                print(e)
                messages.saved_error(request)

        return redirect("Comp-Off_application_form_page")