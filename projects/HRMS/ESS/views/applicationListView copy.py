from datetime import datetime
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from IntelliSync_db.models import CommonMaster,User
from Payroll_db.models import EmployeeMaster
from HRMS_db.models import LeaveApplication
from IS_Nexus.functions.data_conversion import queryset_to_json
from django.db.models import Q, CharField, Value, When, Case
from IS_Nexus.functions.shortcuts import get_or_none


class ApplicationListView(View):
    year_list=CommonMaster.objects.filter(master_type__code='CT-20').values('name','value').order_by('-name')
    month_list=CommonMaster.objects.filter(master_type__code='CT-19').values('name','value').order_by('value')

    def get(self,request):
        current_year=str(request.GET.get('year',datetime.now().year))
        current_month=str(request.GET.get('month',datetime.now().month))
        application_status=request.GET.get('status',None)
        emp_paycode=request.GET.get('emp_paycode',None)
        user=request.user
        applied_on=f'{current_year}-0{current_month}' if int(current_month)<10 else f'{current_year}-{current_month}'
        # data=EmployeeMaster.objects.values('emp_paycode','emp_name').using(f'payroll_db')

        super_user_flag = get_or_none(User, Q(username=user.username) & (Q(is_superuser=True) | Q(is_super_staff=True)))

        leave_data=leave_data=LeaveApplication.objects.all().order_by('-status','-applied_on')

        if super_user_flag:
            pending_application=LeaveApplication.objects.filter(status='Pending').count()
        
        else:
            # leave_data = leave_data.filter(reporting_manager)





        if super_user_flag==None:

            pending_application=LeaveApplication.objects.filter(reporting_manager=user,status='Pending').count()
            
            if application_status==None and emp_paycode==None:
                leave_data=LeaveApplication.objects.filter(reporting_manager=user).order_by('-status','-applied_on')
            else:
                leave_data=LeaveApplication.objects.filter(reporting_manager=user,emp_paycode=emp_paycode.strip(),status=application_status,applied_on__contains=applied_on).order_by('-status','-applied_on')
        else:
            pending_application=LeaveApplication.objects.filter(status='Pending').count()
            
            if application_status==None and emp_paycode==None:
                leave_data=leave_data=LeaveApplication.objects.all().order_by('-status','-applied_on')

            else:
                leave_data=LeaveApplication.objects.filter(emp_paycode=emp_paycode.strip(),status=application_status,applied_on__contains=applied_on).order_by('-status','-applied_on')
        

        context={
            # "data":data,
            "current_year":current_year,
            "current_month":current_month,
            "emp_paycode":emp_paycode,
            "status":application_status,
            "leave_data":leave_data,
            "year_list":self.year_list,
            "month_list":self.month_list,
            "pending_application":pending_application
        }
        return render(request,"applicationApproval.html",context)

    def post(self,request):
        user=request.user
        
        if 'approve_all_submit' in request.POST:
            LeaveApplication.objects.filter(status='Pending').update(status='Approved',approved_by=user,approved_on=datetime.now())
        elif 'reject_all_submit' in request.POST:
            LeaveApplication.objects.filter(status='Pending').update(status='Rejected',cancelled_on=datetime.now(),approved_by=user)
        elif 'approve' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Approved',approved_by=user,approved_on=datetime.now())
        elif 'reject' in request.POST:
            application_id=request.POST.get('application_id')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Rejected',cancelled_on=datetime.now(),approved_by=user)    
        elif 'approve_with_remarks' in request.POST:
            application_id=request.POST.get('id')
            remarks=request.POST.get('remarks')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Approved',approved_by=user,approved_on=datetime.now(),approval_remarks=remarks)    
        elif 'reject_with_remarks' in request.POST:
            application_id=request.POST.get('id')
            remarks=request.POST.get('remarks')
            LeaveApplication.objects.filter(pk=application_id,status='Pending').update(status='Rejected',cancelled_on=datetime.now(),approved_by=user,approval_remarks=remarks)    
        
        return redirect("application_approval_page")

class LeaveApplicationDetails(View):
    def get(self,request):
        id=int(request.GET.get('id'))
        leave_data=LeaveApplication.objects.filter(pk=id)
        return JsonResponse(queryset_to_json(leave_data),safe=False)
