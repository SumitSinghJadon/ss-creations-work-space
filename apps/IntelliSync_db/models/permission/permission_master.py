from django.db import models


class PermissionMaster(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=80, null=True, blank=True, unique=True)
    remarks = models.CharField(max_length=80, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'permission_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name 


class PermissionGroupMaster(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(PermissionMaster)
    remarks = models.CharField(max_length=80, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'permission_group_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name 
