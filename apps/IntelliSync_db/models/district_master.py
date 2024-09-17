from django.db import models
from .state_master import StateMaster
from .country_master import CountryMaster

class DistrictMaster(models.Model):
    country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
    state = models.ForeignKey(StateMaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, default='')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'district_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name   