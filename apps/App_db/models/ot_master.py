from django.db import models


class OTMT(models.Model):
    unit_code = models.CharField(max_length=100)
    dep_code = models.CharField(max_length=100)
    ot_month = models.IntegerField()
    ot_daily = models.IntegerField()    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by =models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)
    def __str__(self):
        return self.unit_code
    
    class Meta:
        db_table ='ot_mt'
        app_label = 'App_db'
    
    