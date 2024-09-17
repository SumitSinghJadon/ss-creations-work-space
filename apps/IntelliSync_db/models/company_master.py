from django.db import models
from IntelliSync_db.models import CountryMaster, StateMaster, DistrictMaster

class CompanyMaster(models.Model):
    name = models.CharField(max_length=200, default='')
    country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
    state = models.ForeignKey(StateMaster, on_delete=models.CASCADE)
    district = models.ForeignKey(DistrictMaster, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=100, default='')
    server_ip = models.CharField(max_length=60, default='')
    gstin = models.CharField(max_length=25, default='')
    address = models.TextField()
    cin = models.CharField(max_length=50)
    pan = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_master'
        app_label = 'IntelliSync_db'
    
    def __str__(self):
        return self.name