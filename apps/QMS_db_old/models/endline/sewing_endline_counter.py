from django.db import models
from IntelliSync_db.models import User
from . import SewingEndlineOutputMt, SewingEndlineOutputDt


class SewingEndlineCounter(models.Model):
    STATUS_CHOICE =(
        ("RFT","PASS"),
        ("D","DEFECT"),
        ("R","REJECT"),
    )
    STATUS_CHOICE2 =(
        ("RCT","RECTIFIED"),
        ("D","DEFECT"), 
        ("R","REJECT"),
    )
    
    rtqm_no         = models.CharField(max_length=30, default='', null=True, blank=True)
    rtqm_dt_no      = models.CharField(max_length=30)
    mt              = models.ForeignKey(SewingEndlineOutputMt,on_delete=models.CASCADE,db_constraint=False)
    dt              = models.ForeignKey(SewingEndlineOutputDt,on_delete=models.CASCADE,db_constraint=False)
    status          = models.CharField(max_length=10,choices=STATUS_CHOICE)
    rectified       = models.CharField(max_length=10,choices=STATUS_CHOICE2,null=True,blank=True)
    entry_date      = models.CharField(max_length=11)
    entry_time      = models.CharField(max_length=5)
    is_active       = models.BooleanField(default=True)
    is_deleted      = models.BooleanField(default=False)
    updated_at      = models.DateTimeField(auto_now=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.rtqm_dt_no}"
    
    class Meta:
        db_table = 'rtqm_counter'
        app_label = 'QMS_db'
    