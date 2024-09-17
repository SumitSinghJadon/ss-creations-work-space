from django.db import models
from .company_master import CompanyMaster


class DepartmentMaster(models.Model):
    company = models.ForeignKey(CompanyMaster, on_delete=models.CASCADE)
    parent = models.CharField(max_length=80, default='')
    name = models.CharField(max_length=80, default='')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'department_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name   