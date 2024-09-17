from django.views import View
from django.shortcuts import redirect, render
from IS_Nexus.functions.data_conversion import queryset_to_json
from IntelliSync_db.models import LocationMaster
from Payroll_db.models import EmployeeMaster,DepartmentMaster,DesignationMaster
from HRMS_db.models import IsEmployeeMaster
from datetime import datetime
class ReportingPerson(View):

    def get(self,request):

        context={
            "employee_list":EmployeeMaster.objects.values('emp_paycode','emp_name').using(f'payroll_db'),
            "department_list":DepartmentMaster.objects.values('dep_code','dep_name'),
            "data":IsEmployeeMaster.objects.all().using('hrms_db')
        }
        
        return render(request,'reporting_person.html',context)
    
    def post(self,request):
        dep_code=request.POST.get('dep_code')
        reporting_person=request.POST.get('emp_code')
        reporting_person=EmployeeMaster.objects.get(emp_paycode=reporting_person)
        data=EmployeeMaster.objects.filter(dep_code=dep_code).values('emp_code','emp_name','emp_paycode','emp_dob','emp_doj','emp_sex','loc_code','des_code','dep_code','emp_email','emp_phn')

        for item in data:
            emp_code=item["emp_code"]
            emp_paycode=item["emp_paycode"]
            emp_name=item["emp_name"]
            doj=item["emp_doj"]
            dob=item["emp_dob"]
            gender="M" if int(item["emp_sex"])==0 else 'F'
            location=item["loc_code"]
            designation=item["des_code"]
            department=item["dep_code"]
            email=item["emp_email"]
            phone_no=item["emp_phn"]

            location=LocationMaster.objects.get(payroll_code=location)
            designation=DesignationMaster.objects.get(des_code=designation)
            department=DepartmentMaster.objects.get(dep_code=department)  
            
            if emp_paycode!=reporting_person:
                IsEmployeeMaster.objects.using('hrms_db').update_or_create(
                    emp_code=emp_code,
                    emp_paycode=emp_paycode,
                    defaults={
                        "emp_name":emp_name,
                        "doj":doj,
                        "dob":dob,
                        "gender":gender,
                        "location":location,
                        "designation":designation,
                        "department":department,
                        "email":email,
                        "phone_no":phone_no,
                        "reporting_person":reporting_person     
                    }
                )
        
        return redirect("reporting_manager")