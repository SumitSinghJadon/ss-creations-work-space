from django.views import View
from django.shortcuts import redirect, render
from IS_Nexus.database.is_hrms import getEmployeeDetails
from datetime import datetime
from HRMS_db.models import LeaveApplication
from IntelliSync_db.models import CommonMaster,User

class WfhView(View):
    year_list=CommonMaster.objects.filter(master_type__code='CT-20').values('name','value').order_by('-name')
    month_list=CommonMaster.objects.filter(master_type__code='CT-19').values('name','value').order_by('value')
    
    def get(self,request):
        current_year=request.GET.get('year',datetime.now().year)
        current_month=request.GET.get('month',datetime.now().month)
        application_status=request.GET.get('application_status',None) if request.GET.get('application_status',None)!='' else None
        emp_paycode=request.user.username
        context=getEmployeeDetails(emp_paycode)

        date=f'{current_year}-{current_month}' if int(current_month)>10 else f'{current_year}-0{current_month}'
        data=LeaveApplication.objects.filter(emp_paycode=emp_paycode,application_type='WFH',applied_on__contains=date) if application_status==None else LeaveApplication.objects.filter(emp_paycode=emp_paycode,application_type='WFH',status=application_status,applied_on__contains=date)
        
        context['leave_data']=data
        context['year_list']=self.year_list
        context['month_list']=self.month_list
        context['current_year']=f'{current_year}'
        context['current_month']=f'{current_month}'
        context['application_status']=application_status
        print(context)
        return render(request,"wfhApplication.html",context)
    
    def post(self,request):
        emp_paycode=request.POST.get("emp_code")
        emp_name=request.POST.get("emp_name")
        unit=request.POST.get("unit")
        department=request.POST.get("department")
        reporting_manager=request.POST.get("reporting_manager")
        application_type=request.POST.get("application_type")
        leave_from=request.POST.get("leave_from")
        leave_till=request.POST.get("leave_till")
        day_part=request.POST.get("day_part")
        day_count=abs(datetime.strptime(leave_from, '%Y-%m-%d') - datetime.strptime(leave_till, '%Y-%m-%d')).days
        visit_location_type=request.POST.get("location_type")
        visit_location=request.POST.get("visit_location")
        purpose_of_visit=request.POST.get("purpose_of_visit")
        status="Pending"
        applied_on=datetime.now()
        LeaveApplication.objects.create(
            emp_paycode=emp_paycode,
            emp_name=emp_name,
            unit=unit,
            dep=department,
            reporting_manager=User.objects.get(pk=reporting_manager),
            application_type=application_type,
            leave_from=leave_from,
            leave_till=leave_till,
            day_part=day_part,
            day_count=day_count,
            visit_location_type=visit_location_type,
            visit_location=visit_location,
            purpose_of_visit=purpose_of_visit,
            status=status,
            applied_on=applied_on
        )
        
        return redirect("WFH_application_form_page")