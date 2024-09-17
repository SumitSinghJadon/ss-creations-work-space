from django.db import models
from IntelliSync_db.models import CommonMaster, FirstLevelMaster
from Payroll_db.models import DepartmentMaster


class TnaActivityMaster(models.Model):
    activity_id = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='tna_activity_id', db_constraint=False)
    activity_group = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='tna_activity_group', db_constraint=False)
    activity_name = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='tna_activity_name', db_constraint=False)
    activity_type = models.CharField(max_length=30)
    activity_responsible = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE, related_name='tna_activity_responsible', db_constraint=False)
    activity_mapping = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tna_activity_master'
        app_label = 'App_db'
        
    def __str__(self):
        return self.activity_name


