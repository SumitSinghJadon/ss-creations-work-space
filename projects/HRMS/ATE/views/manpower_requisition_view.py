from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from IS_Nexus.database.is_hrms import get_payroll_db_name,getEmployeeDetails
from IS_Nexus.functions.shortcuts import pay_db
from datetime import datetime
from IntelliSync_db.models import User,LocationMaster,CommonMaster,SecondLevelMaster ,StatusTrackerMaster
from Payroll_db.models import DepartmentMaster, DesignationMaster,EmployeeMaster
from HRMS_db.models import ManPowerRequisition,ManpowerQualification,ManpowerPreferredResidentLocation
from IS_Nexus.functions import messages
from django.db import connections, transaction


class ManpowerRequisitionView(View):
    def get(self, request):
        if "department" in request.GET:
            department=request.GET.get("department")
            emp_data=EmployeeMaster.objects.filter(dep_code=department).values('emp_paycode','emp_name').using(get_payroll_db_name(datetime.now()))
            emp_data_list = list(emp_data)
            for emp in emp_data_list:
                for key, value in emp.items():
                    if isinstance(value, str):
                        emp[key] = value.strip()
            return JsonResponse(emp_data_list,safe=False)
        elif "emp_code" in request.GET:
            cursor =  connections[get_payroll_db_name(datetime.now())].cursor()    
            emp_code=request.GET.get("emp_code")
            db_name = pay_db(datetime.now().strftime("%Y-%m-%d"))
            query=f"select TOP 1 totrate from {db_name}.dbo.tbemp tbemp INNER JOIN {db_name}.dbo.tbmonth_hist tbmonth_hist ON tbemp.emp_code= tbmonth_hist.emp_code where tbemp.emp_paycode='{emp_code}' order by tbmonth_hist.month_no DESC"
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                totrate = row[0]
                return JsonResponse({'gross_salary':totrate})
            else:
                return JsonResponse({'gross_salary':0})

        else:   
            department_data=DepartmentMaster.objects.all().using(get_payroll_db_name(datetime.now()))
            designation_data=DesignationMaster.objects.all().using(get_payroll_db_name(datetime.now()))
            employee_data=getEmployeeDetails(request.user.username)
            location_data=LocationMaster.objects.values('payroll_code','name')
            qualification_data=CommonMaster.objects.filter(master_type__name="Qualification Master").values('id','name')
            all_emp_data=User.objects.filter(is_reporting_manager=True).values('username','full_name')
            city_data=SecondLevelMaster.objects.filter(master_type__name='City Master').values('id','name')
            requisition_data=ManPowerRequisition.objects.using('default').prefetch_related('manpower_requisition_qualification', 'manpower_requisition_preffered_resident_location').all()
            context={
                "department_data":department_data,
                "designation_data":designation_data,
                "employee_data":employee_data,
                "requisition_data":requisition_data,
                "all_emp_data":all_emp_data[:30],
                "location_data":location_data,
                "qualification_data":qualification_data,
                "city_data":city_data
            }
            return render(request,"manpower_requition.html",context)


    def post(self, request):
        if all(param in request.POST for param in ['application_id', 'suggested_salary_range', 'remarks']):
            application_id=request.POST.get('application_id')
            suggested_salary_range=request.POST.get('suggested_salary_range')
            remarks=request.POST.get('remarks')
            manpower_requisition = ManPowerRequisition.objects.filter(pk=application_id).first()
                
            if manpower_requisition:
                status = None

                if manpower_requisition.user.reporting_manager == request.user:
                    status = 'AHOD'
                elif request.user.is_super_staff:
                    status = 'AM'
                if status:
                    manpower_requisition.status = status
                    manpower_requisition.suggested_salary_range=suggested_salary_range
                    manpower_requisition.remarks=remarks
                    manpower_requisition.save()

                    # Insert into StatusTrackerMaster
                    StatusTrackerMaster.objects.create(
                        page='MPR',
                        application_id=manpower_requisition.id,
                        status=status,
                        user=request.user
                    )
                return JsonResponse({'success': True, 'message': 'Approved updated successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'No ManPowerRequisition object found with the given application_id.'})     
        elif 'reject_application_id' in request.POST:
            application_id=request.POST.get('reject_application_id')
            manpower_requisition = ManPowerRequisition.objects.filter(pk=application_id).first()
            
            if manpower_requisition:
                status = None

                if manpower_requisition.user.reporting_manager == request.user:
                    status = 'RHOD'
                elif request.user.is_super_staff:
                    status = 'RM'

                if status:
                    manpower_requisition.status = status
                    manpower_requisition.save()

                    # Insert into StatusTrackerMaster
                    StatusTrackerMaster.objects.create(
                        page='MPR',
                        application_id=manpower_requisition.id,
                        status=status,
                        user=request.user
                    )
                    return JsonResponse({'success': True, 'message': 'Rejected successfully.'})
                
            else:
                return JsonResponse({'success': False, 'message': 'No ManPowerRequisition object found with the given application_id.'}) 
        else:
            try:
                with transaction.atomic():
                    user = request.user
                    request_type = request.POST.get('request_type')
                    department_for = DepartmentMaster.objects.using(get_payroll_db_name(datetime.now())).filter(pk=request.POST.get('department_for')).first()
                    sub_department = request.POST.get('sub_department')
                    designation_for = DesignationMaster.objects.using(get_payroll_db_name(datetime.now())).filter(pk=request.POST.get('designation_for')).first()
                    replacement_employee = None
                    employee_salary=request.POST.get('employee_salary')
                    if "replacement_for" in request.POST:
                        replacement_employee = User.objects.using('intellisync_db').get(username=request.POST.get('replacement_for'))
                    justification = request.POST.get('justification')
                    job_description=request.POST.get('job-description')
                    report_to = User.objects.using('intellisync_db').get(username=request.POST.get('report_to'))
                    job_location = LocationMaster.objects.using('intellisync_db').get(payroll_code=request.POST.get('job_location'))
                    salary_range = request.POST.get('salary_from')+" - "+request.POST.get('salary_to')
                    exp_year_range = request.POST.get('exp_year_from')+" - "+request.POST.get('exp_year_to')
                    special_skill_required = request.POST.get('special_skill_required')
                    age_range = request.POST.get('min_age')+" - "+request.POST.get('max_age')
                    preferred_gender = request.POST.get('preferred_gender')
                    
                    # Retrieve qualification and preferred resident locations IDs from POST data
                    qualification_ids = request.POST.getlist('qualification')
                    preferred_resident_location_ids = request.POST.getlist('preferred_resident_location')
                    
                    # Retrieve CommonMaster objects for qualification
                    qualifications = CommonMaster.objects.filter(id__in=qualification_ids)
                    
                    # Retrieve SecondLevelMaster objects for preferred resident locations
                    preferred_resident_locations = SecondLevelMaster.objects.filter(id__in=preferred_resident_location_ids)
                    
                    # Create ManPowerRequisition instance with ManyToMany fields
                    manpower_requisition = ManPowerRequisition.objects.create(
                        user=user,
                        request_type=request_type,
                        department_for=department_for,
                        sub_department=sub_department,
                        designation_for=designation_for,
                        replacement_employee=replacement_employee,
                        employee_salary=employee_salary,
                        justification=justification,
                        report_to=report_to,
                        job_location=job_location,
                        salary_range=salary_range,
                        exp_year_range=exp_year_range,
                        age_range=age_range,
                        special_skill_required=special_skill_required,
                        job_description=job_description
                    )

                    if request.user.is_reporting_manager:
                        manpower_requisition.status = 'AHOD'

                    StatusTrackerMaster.objects.create(
                        page='MPR',
                        application_id=manpower_requisition.id,
                        status='AHOD' if request.user.is_reporting_manager else 'P',
                        user=request.user
                    )

                    if preferred_gender:
                        manpower_requisition.preferred_gender = preferred_gender
                    
                    # Create ManpowerQualification instances
                    for qualification in qualifications:
                        ManpowerQualification.objects.create(manpower=manpower_requisition, qualification=qualification)

                    # Create ManpowerPreferredResidentLocation instances
                    for location in preferred_resident_locations:
                        ManpowerPreferredResidentLocation.objects.create(manpower=manpower_requisition, preferred_resident_location=location)

                    messages.saved(request)

                    return redirect("manpower_requisition_form_page")
            except Exception as e:
                # Rollback the transaction if an exception occurs
                transaction.rollback()
                messages.saved_error(request)
                return redirect("manpower_requisition_form_page")


class ManpowerStatusTracker(View):
    def get(self,request):
        mpr_id=int(request.GET.get('id'))
        data=StatusTrackerMaster.objects.filter(page='MPR',application_id=mpr_id)
        serialized_data = []
        for item in data:
            serialized_item = {
                'page': item.page,
                'application_id': item.application_id,
                'status': item.get_status_display(),  # Use get_status_display() to retrieve the display value
                'user': item.user.full_name,
                'paycode': item.user.username,
                'created_at': item.created_at.strftime("%d-%m-%Y %I:%M %p")
            }
            serialized_data.append(serialized_item)
        return JsonResponse(serialized_data,safe=False)