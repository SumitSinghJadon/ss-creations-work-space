from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from django.db.models import Q
from django.template.loader import render_to_string
from datetime import datetime
from IS_Nexus.database.is_hrms import hrms_mailer
from IntelliSync_db.models import CommonMaster, User,LocationPermission,LocationMaster,UserPermissionMaster
from HRMS_db.models import LeaveApplication
from IS_Nexus.functions.data_conversion import queryset_to_json
from IS_Nexus.functions.shortcuts import formate_date
from Payroll_db.models.employee_master import EmployeeMaster
from django.contrib import messages

class ApplicationListView(View):
    def get(self, request):
        user_list   = User.objects.using('intellisync_db').all().filter(is_active=True)
        year_list   = CommonMaster.objects.filter(master_type__code='CT-20').values('name', 'value').order_by('-name')
        month_list  = CommonMaster.get_month_list()

        eid = request.GET.get('eid')
        from_date = request.GET.get('from_date')
        till_date = request.GET.get('till_date')
        status = request.GET.get('status')

        application_list = LeaveApplication.objects.all()
        combined_filters = None
        if eid or from_date or till_date or status:
            combined_filters = Q()

        if eid:
            combined_filters &= Q(user=eid)

        if from_date:
            from_date = formate_date(f"{from_date}T00:00")
            combined_filters &= Q(from_date__gte=from_date)

        if till_date:
            till_date = formate_date(f"{till_date}T00:00")
            combined_filters &= Q(till_date__lte=till_date)

        if status:
            combined_filters &= Q(status=status)

        if combined_filters != None:
            application_list = application_list.filter(combined_filters)
        else:
            application_list=application_list.filter(status='Pending')

        context = {
            'user_list'       : user_list,
            'year_list'       : year_list,
            'month_list'      : month_list,
            'application_list': application_list
        }
        return render(request,"applicationApproval.html",context)


    def post(self,request):
        user=request.user

        if 'approve_all_submit' in request.POST:
            LeaveApplication.objects.filter(status='Pending').update(status='Approved',updated_by=user,approved_on=datetime.now())

        elif 'reject_all_submit' in request.POST:
            LeaveApplication.objects.filter(status='Pending').update(status='Rejected',approved_on=datetime.now(),updated_by=user)

        elif 'approve' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Approved',updated_by=user,approved_on=datetime.now())
            
            url = self.request.get_host()
            data=LeaveApplication.objects.get(pk=application_id)
            
            hr_mail = LocationPermission.objects.filter(
                location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode=data.user.username).loc_code), 
                user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
            ).values_list('user__email',flat=True).exclude(user__email=None)
            try:
                hrms_mailer(f'Approved Application Notification - { data.user.full_name } { data.user.username }', render_to_string('mailApplicationApproved.html', {'application_list': data,"url":url}), [item for item in hr_mail])
            except Exception as e:
                messages.warning(request,"Unable to send email to your head of department")

        elif 'reject' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Rejected',approved_on=datetime.now(),updated_by=user)    

        elif 'approve_with_remarks' in request.POST:
            application_id=request.POST.get('id')
            remarks=request.POST.get('remarks')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Approved',updated_by=user,approved_on=datetime.now(),remarks=remarks)    
            url = self.request.get_host()
            data=LeaveApplication.objects.get(pk=application_id)
            
            hr_mail = LocationPermission.objects.filter(
                location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode=data.user.username).loc_code), 
                user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
            ).values_list('user__email',flat=True).exclude(user__email=None)
            try:
                hrms_mailer(f'Approved Application Notification - { data.user.full_name } { data.user.username }', render_to_string('mailApplicationApproved.html', {'application_list': data,"url":url}), [item for item in hr_mail])
            except Exception as e:
                messages.warning(request,"Unable to send email to your head of department")
        
        elif 'reject_with_remarks' in request.POST:
            application_id=request.POST.get('id')
            remarks=request.POST.get('remarks')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Rejected',approved_on=datetime.now(),updated_by=user,remarks=remarks)    
        
        return redirect("application_approval_page")

class LeaveApplicationDetails(View):
    def get(self,request):
        id=int(request.GET.get('id'))
        leave_data=LeaveApplication.objects.filter(pk=id)
        return JsonResponse(queryset_to_json(leave_data),safe=False)

class ApprovalOverMail(View):

    def get(self,request):
        emp_code=request.GET.get("emp")
        application_id=request.GET.get("id")
        user=User.objects.get(username=emp_code)
        LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Approved',updated_by=user,approved_on=datetime.now())
        url = self.request.get_host()
        data=LeaveApplication.objects.get(pk=application_id)
            
        hr_mail = LocationPermission.objects.filter(
            location=LocationMaster.objects.get(payroll_code=EmployeeMaster.objects.get(emp_paycode=data.user.username).loc_code), 
            user__in=UserPermissionMaster.objects.filter(permission__permission__code='HRA').values_list('user__id')
        ).values_list('user__email',flat=True).exclude(user__email=None)
        try:
            hrms_mailer(f'Approved Application Notification - { data.user.full_name } { data.user.username }', render_to_string('mailApplicationApproved.html', {'application_list': data,"url":url}), [item for item in hr_mail])
        except Exception as e:
            messages.error(request,"Unable to send email to your head of department")
        return HttpResponse('Application Approved')
    
class RejectOverMail(View):

    def get(self,request):
        emp_code=request.GET.get("emp")
        application_id=request.GET.get("id")
        user=User.objects.get(username=emp_code)
        LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Rejected',updated_by=user,approved_on=datetime.now())  
        return HttpResponse('Application Rejected')