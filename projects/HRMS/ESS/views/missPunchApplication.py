from django.views import View
from django.shortcuts import redirect, render
from HRMS_db.models import LeaveApplication
from datetime import datetime, timedelta
from IS_Nexus.database.is_hrms import getEmployeeDetails, hrms_mailer
from IntelliSync_db.models import LocationMaster ,LocationPermission ,UserPermissionMaster , CommonMaster
from Payroll_db.models import EmployeeMaster 
from IS_Nexus.functions import messages
from .params import date_parm
from django.template.loader import render_to_string


class MissPunchView(View):
    year_list=CommonMaster.objects.filter(master_type__code='CT-20').values('name','value').order_by('-name')
    month_list=CommonMaster.objects.filter(master_type__code='CT-19').values('name','value').order_by('value')
    
    def get(self,request):
        
        employee = getEmployeeDetails(request.user.username)
        leave_list = LeaveApplication.objects.filter(user=request.user,application_type='Miss Punch')
        
        context = {
            'employee' : employee['data'],
            'leave_list' : leave_list,
            'min_date' : datetime.now()-timedelta(days=date_parm)
        }
        
        return render(request,"missPunchApplication.html",context)
    
    def post(self,request):
        if 'cancel_application' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Cancelled',cancelled_on=datetime.now())   
        else:
            from_date=request.POST.get("leave_from")
            mis_in_time=request.POST.get("miss_punch_in")
            day_part=request.POST.get("day_part")
            reason=request.POST.get("reason")
            department=request.POST.get("department")
            applied_on=datetime.now()

            try:
                data = LeaveApplication.objects.create(
                    user = request.user,
                    dep = department,
                    application_type = 'Miss Punch',
                    from_date = from_date,
                    day_part = day_part,
                    time=mis_in_time,
                    reason = reason,
                    status = 'Pending',
                    applied_on=applied_on 
                )
                messages.saved(request)

                hr_mail = LocationPermission.objects.filter(
                    location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode=request.user.username).loc_code), 
                    user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
                ).values_list('user__username','user__email').exclude(user__email=None)

                try:
                    hrms_mailer(f'Miss Punch Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":request.user.reporting_manager.username}), [request.user.reporting_manager.email])

                    hrms_mailer(f'Miss Punch Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":hr_mail[0][0]}), [hr_mail[0][1]])
                
                except Exception as e:
                    messages.error(request,"Unable to send email to your head of department")

            except Exception as e:
                print(e)
                messages.saved_error(request)
        
        return redirect("miss_punch_application_form_page")