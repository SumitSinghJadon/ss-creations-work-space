from django.db import models


class CountryMaster(models.Model):
    code = models.CharField(max_length=4, default='')
    name = models.CharField(max_length=50, default='')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'country_master'
        app_label = 'IntelliSync_db'
    
    def __str__(self):
        return self.name

