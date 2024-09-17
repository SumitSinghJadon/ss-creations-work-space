from django.db import models
from .state_master import StateMaster
from .country_master import CountryMaster
from .company_master import CompanyMaster
from .district_master import DistrictMaster


class LocationMaster(models.Model):
    company = models.ForeignKey(CompanyMaster, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
    state = models.ForeignKey(StateMaster, on_delete=models.CASCADE)
    district = models.ForeignKey(DistrictMaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, default='')
    gstin = models.CharField(max_length=20)
    address = models.TextField()

    payroll_code = models.CharField(max_length=20, null=True, blank=True)
    erp_code = models.CharField(max_length=20, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'location_master'
        unique_together = ('company', 'name')
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name   
