from django.db import models


class ManpowerplanMT(models.Model):
    mmr_code = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=100)
    manpower = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by =models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)
    def __str__(self):
        return self.dept
    
    class Meta:
        db_table ='manpower_plan'
        app_label = 'App_db'
    
    