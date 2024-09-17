from django.db import models
from .project_master import ProjectMaster


class ModuleMaster(models.Model):
    project = models.ForeignKey(ProjectMaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    dashboard_url = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='modules/')
    separate_menu = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'module_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name
