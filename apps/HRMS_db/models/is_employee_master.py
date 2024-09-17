from django.db import models
from IntelliSync_db.models import LocationMaster
from Payroll_db.models import DesignationMaster,DepartmentMaster,EmployeeMaster

class DepartmentHead(models.Model):
    department = models.CharField(max_length=80)
    head       = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table  = 'department_head'
        app_label = 'HRMS_db'


class IsEmployeeMaster(models.Model):
    emp_code=models.CharField(max_length=100, unique=True)
    emp_paycode=models.CharField(max_length=100, unique=True)
    emp_name=models.CharField(max_length=300, blank=False, null=False)
    doj=models.DateField(blank=False, null=False)
    dob=models.DateField(blank=False, null=False)
    gender=models.CharField(max_length=300, blank=False, null=False)
    location=models.ForeignKey(LocationMaster,on_delete=models.DO_NOTHING,db_constraint=False, db_column='location')
    designation=models.ForeignKey(DesignationMaster,on_delete=models.DO_NOTHING,db_constraint=False, db_column='designation')
    department=models.ForeignKey(DepartmentMaster,on_delete=models.DO_NOTHING,db_constraint=False, db_column='department')
    email=models.CharField(max_length=300, blank=False, null=False)
    phone_no=models.CharField(max_length=300, blank=False, null=False)
    reporting_person = models.ForeignKey(EmployeeMaster, on_delete=models.DO_NOTHING, db_constraint=False, db_column='reporting_person', to_field='emp_paycode', blank=False, null=False)

    class Meta:
        managed = False
        db_table  = 'is_employee_master'
        app_label = 'HRMS_db'

