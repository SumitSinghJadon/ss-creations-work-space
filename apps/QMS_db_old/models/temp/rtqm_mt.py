from django.db import models
from IntelliSync_db.models import CommonMaster,FirstLevelMaster,LocationMaster,get_next_number


class RtqmMt(models.Model):
    rtqm_no         = models.CharField(max_length=30, unique=True)
    buyer_code      = models.CharField(max_length=255)
    buyer_name      = models.CharField(max_length=255)
    style           = models.CharField(max_length=255)
    ourref          = models.CharField(max_length=255)
    color           = models.CharField(max_length=255)
    total_quantity  = models.IntegerField(default=0)
    unit            = models.ForeignKey(LocationMaster, on_delete=models.CASCADE ,db_constraint=False)
    floor           = models.ForeignKey(CommonMaster, on_delete=models.CASCADE ,db_constraint=False)
    line            = models.ForeignKey(FirstLevelMaster,on_delete=models.CASCADE ,db_constraint=False)
    is_active       = models.BooleanField(default=True)
    is_deleted      = models.BooleanField(default=False)
    updated_at      = models.DateTimeField(auto_now=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.buyer_name} - {self.rtqm_no} [ {self.style} ]"
    
    class Meta:
        unique_together = ('buyer_code','style','ourref','color')
        db_table = 'rtqm_mt'
        app_label = 'QMS_db'
    