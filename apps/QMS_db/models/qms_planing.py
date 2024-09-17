from django.db import models
from IntelliSync_db.models import LocationMaster ,CommonMaster,FirstLevelMaster 

class QmsPlaning(models.Model):
    buyer = models.CharField(max_length=100)
    buyer_name = models.CharField(max_length=100 ,null=True,blank=True)
    ourref = models.CharField(max_length=100)
    styleno = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    delvdate = models.DateField()
    unit = models.ForeignKey(LocationMaster, on_delete=models.CASCADE ,db_constraint=False)
    floor = models.ForeignKey(CommonMaster, on_delete=models.CASCADE ,db_constraint=False)
    line = models.ForeignKey(FirstLevelMaster,on_delete=models.CASCADE ,db_constraint=False)
    quantity = models.IntegerField()
    planing_no = models.CharField(max_length=50,blank=True,null=True)
    planing_date = models.DateField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    class Meta:
        db_table = 'sewing_planning'
        app_label = 'QMS_db'
        
    def __str__(self):
        return self.style_no
