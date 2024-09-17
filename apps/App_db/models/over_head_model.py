from django.db import models


class OverHeadMT(models.Model):
    head_id = models.CharField(max_length=100)
    unit_name = models.CharField(max_length=100)
    daily_cost = models.IntegerField()
    monthly_cost = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_by = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.unit_name
    
    class Meta:
        db_table ='over_head_mt'
        app_label = 'App_db'
    
    