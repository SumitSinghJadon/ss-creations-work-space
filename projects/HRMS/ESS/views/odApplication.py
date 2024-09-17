from django.views import View
from django.shortcuts import redirect, render
from IS_Nexus.database.is_hrms import getEmployeeDetails, hrms_mailer
from datetime import datetime, timedelta
from HRMS_db.models import LeaveApplication
from IS_Nexus.functions import messages
from IntelliSync_db.models import LocationMaster ,LocationPermission ,UserPermissionMaster , CommonMaster
from Payroll_db.models import EmployeeMaster
from .params import date_parm
from django.template.loader import render_to_string

class ODView(View):
    year_list=CommonMaster.objects.filter(master_type__code='CT-20').values('name','value').order_by('-name')
    month_list=CommonMaster.objects.filter(master_type__code='CT-19').values('name','value').order_by('value')
    
    def get(self,request):
        employee = getEmployeeDetails(request.user.username)
        leave_list = LeaveApplication.objects.filter(user=request.user,application_type='OD')

        context = {
            'employee' : employee['data'],
            'min_date' : datetime.now()-timedelta(days=date_parm),
            'leave_list' : leave_list
        }
        return render(request,"odApplication.html",context)

    
    def post(self,request):
        if 'cancel_application' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Cancelled',cancelled_on=datetime.now())   
        else:
            department=request.POST.get("department")
            from_date=request.POST.get("from_date")
            till_date=request.POST.get("till_date")
            day_count = abs(datetime.strptime(from_date, '%Y-%m-%dT%H:%M') - datetime.strptime(till_date, '%Y-%m-%dT%H:%M')).days + 1
            visit_location_type=request.POST.get("location_type")
            visit_location=request.POST.get("visit_location")
            purpose_of_visit=request.POST.get("purpose_of_visit")
            applied_on=datetime.now()

            try:
                data=LeaveApplication.objects.create(
                    user = request.user,
                    dep = department,
                    application_type = 'OD',
                    from_date=from_date,
                    till_date=till_date,
                    day_count=day_count,
                    visit_location_type=visit_location_type,
                    address=visit_location,
                    reason=purpose_of_visit,
                    status='Pending',
                    applied_on=applied_on
                )
                messages.saved(request)
                
                hr_mail = LocationPermission.objects.filter(
                    location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode=request.user.username).loc_code), 
                    user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
                ).values_list('user__username','user__email').exclude(user__email=None)

                try:
                    hrms_mailer(f'On Duty Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":request.user.reporting_manager.username}), [request.user.reporting_manager.email])

                    hrms_mailer(f'On Duty Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":hr_mail[0][0]}), [hr_mail[0][1]])
                
                except Exception as e:
                    messages.error(request,"Unable to send email to your head of department")

                
            except Exception as e:
                print(e)
                messages.saved_error(request)
        return redirect("od_application_form_page")
    
