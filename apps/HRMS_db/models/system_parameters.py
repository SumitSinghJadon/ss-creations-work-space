from django.db import models

class SystemParameter(models.Model):
    parameter_name = models.CharField(max_length=255, blank=True, null=True)
    min_limit = models.CharField(max_length=10, blank=True, null=True)
    max_limit = models.CharField(max_length=10, blank=True, null=True)
    parameter_value = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)
    stamp = models.DateTimeField(auto_now_add=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    perm_value = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'system_parameters'
        app_label = 'HRMS_db'
