from django.db import models

class EnergyCost(models.Model):
    unit = models.CharField(max_length=50)
    head = models.CharField(max_length=50)
    sub_head = models.CharField(max_length=50)
    date = models.DateField()
    reading = models.FloatField(default=0.00,null=True)
    cons_hr = models.FloatField(default=0.00,null=True)
    consumption = models.FloatField(default=0.00,null=True)
    fuel_consumed = models.FloatField(default=0.00,null=True)
    running_unit = models.FloatField(default=0.00,null=True)
    kwh_reading = models.FloatField(default=0.00, null=True)
    multiplier = models.FloatField(default=0.00, null=True)
    unit_consumed = models.FloatField(default=0.00, null=True)
    unit_consumed_kvah = models.FloatField(default=0.00, null=True)
    unit_consumed_kwh = models.FloatField(default=0.00, null=True)
    kvah_reading = models.FloatField(default=0.00, null=True)
    power_factor = models.FloatField(default=0.00, null=True)
    rate = models.FloatField(default=0.00)
    energy_value = models.FloatField(default=0.00) 

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by =models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)
    
    class Meta:
        app_label = 'App_db'  
        db_table = 'energy'