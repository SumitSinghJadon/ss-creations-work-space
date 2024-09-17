from django.db import models
from IntelliSync_db.models import User,LocationMaster,CommonMaster,SecondLevelMaster
from Payroll_db.models import DepartmentMaster,DesignationMaster 


class ManPowerRequisition(models.Model):
    
    request_type_list = (
        ('N', 'New'),
        ('R', 'Replacement'),
        ('A', 'Any')
    )
    
    gender_list = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('A', 'Any')
    )

    status_list = (
        ('P', 'Pending'),
        ('AHOD', 'Approved by HOD'),
        ('RHOD','Rejected by HOD'),
        ('AM', 'Approved by Management'),
        ('RM','Rejected by Management')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manpower_requisition_user', db_constraint=False)
    request_type = models.CharField(max_length=20, blank=True, null=True, choices=request_type_list)
    department_for = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE, related_name='manpower_requisition_department_for', db_constraint=False)
    sub_department = models.CharField(max_length=100, blank=True, null=True)
    designation_for = models.ForeignKey(DesignationMaster, on_delete=models.CASCADE, related_name='manpower_requisition_designation_for', db_constraint=False, blank=True, null=True)
    replacement_employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manpower_requisition_replacement_for', db_constraint=False, blank=True, null=True)
    employee_salary=models.CharField(max_length=100, blank=True, null=True)
    justification = models.TextField(blank=True, null=True)
    report_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manpower_requisition_report_to', db_constraint=False)
    job_location = models.ForeignKey(LocationMaster, on_delete=models.CASCADE, related_name='manpower_requisition_job_location', db_constraint=False)
    status = models.CharField(max_length=10, default='P', choices=status_list)
    no_of_positions=models.CharField(max_length=10,null=True,blank=True)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    suggested_salary_range = models.CharField(max_length=100, blank=True, null=True)
    exp_year_range = models.CharField(max_length=10, blank=True, null=True)
    age_range = models.CharField(max_length=10, blank=True, null=True)
    special_skill_required = models.TextField(blank=True, null=True)
    preferred_gender = models.CharField(max_length=20, default='A', choices=gender_list)
    remarks = models.TextField(blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'manpower_requisition'
        app_label = 'HRMS_db'



class ManpowerQualification(models.Model):
    manpower = models.ForeignKey(ManPowerRequisition,db_constraint=False,on_delete=models.CASCADE,related_name='manpower_requisition_qualification')
    qualification = models.ForeignKey(CommonMaster,db_constraint=False,on_delete=models.CASCADE)

    class Meta:
        db_table='manpower_requisition_degree'
        app_label='HRMS_db'


class ManpowerPreferredResidentLocation(models.Model):
    manpower = models.ForeignKey(ManPowerRequisition,db_constraint=False,on_delete=models.CASCADE,related_name='manpower_requisition_preffered_resident_location')
    preferred_resident_location = models.ForeignKey(SecondLevelMaster,db_constraint=False,on_delete=models.CASCADE)

    class Meta:
        db_table='manpower_requisition_location'
        app_label='HRMS_db'

