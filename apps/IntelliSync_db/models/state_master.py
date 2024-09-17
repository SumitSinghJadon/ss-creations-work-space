from django.db import models
from IntelliSync_db.models import CountryMaster


class StateMaster(models.Model):
    country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'state_master'
        app_label = 'IntelliSync_db'
    
    def __str__(self):
        return self.name
