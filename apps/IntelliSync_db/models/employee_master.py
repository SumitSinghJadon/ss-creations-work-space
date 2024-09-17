from django.db import models
from .department_master import DepartmentMaster
from .designation_master import DesignationMaster
from .district_master import DistrictMaster
from IntelliSync_db.models import User


class EmployeeMaster(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100,default='')
    department = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    designation = models.ForeignKey(DesignationMaster, on_delete=models.CASCADE)
    district = models.ForeignKey(DistrictMaster, on_delete=models.CASCADE)
    senior = models.CharField(max_length=80, default='')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employee_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name}'
