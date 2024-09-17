from django.db import models
from IntelliSync_db.models import User
from .page_permission_master import PagePermissionMaster


class UserPermissionMaster(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False)
    permission = models.ForeignKey(PagePermissionMaster, on_delete=models.SET_NULL,null=True,blank=True,db_constraint=False)
    
    class Meta:
        db_table = 'user_permission_master'
        app_label = 'IntelliSync_db'
        unique_together = ('user', 'permission')

    def __str__(self):
        return f"{self.user} ({self.permission})"

