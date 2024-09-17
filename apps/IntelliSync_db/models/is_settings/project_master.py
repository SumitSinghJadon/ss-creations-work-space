from django.db import models


class ProjectMaster(models.Model):
    company = models.ForeignKey('CompanyMaster', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)
    server_port = models.IntegerField(default=8000)
    separate_menu = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'project_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name

