from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from IntelliSync_db.manager import UserManager
from django.contrib.auth.hashers import make_password


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=80, unique=True)
    full_name = models.CharField(max_length=40)
    reporting_manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,db_constraint=False)
    location = models.ForeignKey('LocationMaster', null=True, blank=True, on_delete=models.SET_NULL, db_constraint=False)
    email = models.EmailField(null=True, blank=True)
    is_reporting_manager = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_super_staff = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user_master'
        app_label = 'IntelliSync_db'

    def save(self, *args, **kwargs):
        user = User.objects.filter(username = self.username, password = self.password)
        if not user:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_or_none(self, *args, **kwargs):
        try:
            return self.objects.get(**args)
        except self.DoesNotExist:
            return None

    USERNAME_FIELD = 'username'
    objects = UserManager()

