from django.db import models
from ..is_settings.menu_master import MenuMaster
from .permission_master import PermissionMaster


class PagePermissionMaster(models.Model):
    page = models.ForeignKey(MenuMaster, on_delete=models.CASCADE) 
    permission = models.ForeignKey(PermissionMaster, on_delete=models.CASCADE) 
    
    is_active = models.BooleanField(default=True) 
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at') 
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at') 

    class Meta:
        db_table = 'page_permission_master'
        app_label = 'IntelliSync_db'
        unique_together = ('page', 'permission')

    def __str__(self):
        return self.page.name

