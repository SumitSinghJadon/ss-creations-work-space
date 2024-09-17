from django.views import View
from django.shortcuts import redirect, render
from IS_Nexus.database.is_hrms import getEmployeeDetails,get_payroll_db_name, hrms_mailer
from datetime import datetime, timedelta
from HRMS_db.models import LeaveApplication,SystemParameter
from IS_Nexus.functions import messages
from IntelliSync_db.models import LocationMaster ,LocationPermission ,UserPermissionMaster , CommonMaster
from Payroll_db.models import EmployeeMaster ,LeaveBalance
from .params import date_parm
from django.template.loader import render_to_string

class LeaveView(View):
    def get(self,request):
        leave_apply_time=SystemParameter.objects.filter(parameter_name='leave_apply_time', condition='Y').first()
        form_visibilty=True
        
        if leave_apply_time:
            current_time=datetime.now().time()
            min=datetime.strptime(leave_apply_time.min_limit, '%H:%M').time()
            max=datetime.strptime(leave_apply_time.max_limit, '%H:%M').time()

            if min and max and min <= current_time <= max: 
                form_visibilty=True
            else:
                form_visibilty=False  
                             
        year_list=CommonMaster.objects.filter(master_type__code='CT-20').values('name','value').order_by('-name')
        month_list=CommonMaster.objects.filter(master_type__code='CT-19').values('name','value').order_by('value')
        employee = getEmployeeDetails(request.user.username)
        leave_list = LeaveApplication.objects.filter(user=request.user, application_type='Leave')
        current_month=datetime.now().month
        
        if current_month < 4:
            if current_month == 1 :
                current_month = '13'
            elif current_month == 2 :
                current_month = '14'
            elif current_month == 3 :
                current_month = '15'
        leave_balance=None

        try:
            leave_balance=LeaveBalance.objects.using(get_payroll_db_name(datetime.now())).filter(emp_code=employee["data"]["emp_code"],month_no=current_month).values('bsl','bcl','bel').first()

        except Exception as e:
            print('\n\n',e,'\n\n')

        context = {
            'employee' : employee['data'],
            'min_date' : datetime.now()-timedelta(days=date_parm),
            'leave_list' : leave_list,
            'year_list' : year_list,
            'month_list' : month_list,
            'leave_balance' : leave_balance,
            'form_visibility' : form_visibilty
        }
        return render(request,"leaveApplication.html",context)


    def post(self,request):
        if 'cancel_application' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Cancelled',cancelled_on=datetime.now())   
        else:
            from_date =request.POST.get("from_date")
            till_date =request.POST.get("till_date")
            day_part = request.POST.get("day_part")
            address = request.POST.get("address")
            phone = request.POST.get("phone")
            leave_type = request.POST.get("leave_type")
            reason = request.POST.get("reason")
            attachment = request.FILES.get("attachment")
            department=request.POST.get("department")
            day_count = abs(datetime.strptime(from_date, '%Y-%m-%d') - datetime.strptime(till_date, '%Y-%m-%d')).days + 1
            applied_on = datetime.now()
            try:
                data = LeaveApplication.objects.create(
                    user = request.user,
                    dep = department,
                    application_type = 'Leave',
                    leave_type = leave_type,
                    from_date = from_date,
                    till_date = till_date,
                    day_part = day_part,
                    day_count = day_count, 
                    reason = reason, 
                    address = address, 
                    mobile_number = phone,
                    status = 'Pending',
                    attachment = attachment,
                    applied_on=applied_on 
                )
                
                messages.saved(request)
                
                hr_mail = LocationPermission.objects.filter(
                    location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode=request.user.username).loc_code), 
                    user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
                ).values_list('user__username','user__email').exclude(user__email=None)

                try:
                    hrms_mailer(f'Leave Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":request.user.reporting_manager.username}), [request.user.reporting_manager.email])

                    hrms_mailer(f'Leave Application Notification - {request.user.full_name} {request.user.username}', render_to_string('mailApplicationApproval.html', {'application_list': LeaveApplication.objects.get(pk=data.pk),"url":self.request.get_host(),"rpr_hr_paycode":hr_mail[0][0]}), [hr_mail[0][1]])
                except Exception as e:
                    messages.error(request,"Unable to send email to your head of department")
            except Exception as e:
                print(e)
                messages.saved_error(request)

        return redirect("leave_application_form_page")