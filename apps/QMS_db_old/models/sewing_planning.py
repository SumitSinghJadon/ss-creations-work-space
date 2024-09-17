from django.db import models
from IntelliSync_db.models import LocationMaster, CommonMaster, FirstLevelMaster 


class SewingPlanning(models.Model):
    buyer = models.CharField(max_length=100)
    buyer_name = models.CharField(max_length=100 ,null=True,blank=True)
    style_no = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    ourref = models.CharField(max_length=100)
    delvdate = models.DateField()
    unit = models.ForeignKey(LocationMaster, on_delete=models.CASCADE ,db_constraint=False)
    floor = models.ForeignKey(CommonMaster, on_delete=models.CASCADE ,db_constraint=False)
    line = models.ForeignKey(FirstLevelMaster,on_delete=models.CASCADE ,db_constraint=False)
    quantity = models.IntegerField()
    planning_no = models.CharField(max_length=50,blank=True,null=True)
    planning_date = models.DateField()

    is_closed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sewing_planning'
        app_label = 'QMS_db'
        
    def __str__(self):
        return self.style_no
