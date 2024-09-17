from django.db import models
from IntelliSync_db.models import User
from QMS_db.models import RtqmMt,RtqmDt ,ObDetail,DefectMaster
from QMS_db.models.endline.rtqm_counter import RtqmCounter 


class RtqmDefectDT(models.Model):
    rtqm_dt_no      = models.CharField(max_length=30)
    rtqm_no         = models.CharField(max_length=50)
    rtqm_mt         = models.ForeignKey(RtqmMt,on_delete=models.CASCADE,db_constraint=False)
    rtqm_dt         = models.ForeignKey(RtqmDt,on_delete=models.CASCADE,db_constraint=False)
    rtqm_counter    = models.ForeignKey(RtqmCounter,on_delete=models.CASCADE,db_constraint=False,null=True,blank=True) 
    ob_detail       = models.ForeignKey(ObDetail,on_delete=models.CASCADE,db_constraint=False)
    defect          = models.ForeignKey(DefectMaster,on_delete=models.CASCADE,db_constraint=False)
    ob_name         = models.CharField(max_length=255, default='', null=True, blank=True)
    defect_name     = models.CharField(max_length=255, default='', null=True, blank=True)
    sb_x            = models.CharField(max_length=255, default='', null=True, blank=True)
    sb_y            = models.CharField(max_length=255, default='', null=True, blank=True)
    sf_x            = models.CharField(max_length=255, default='', null=True, blank=True)
    sf_y            = models.CharField(max_length=255, default='', null=True, blank=True)
    size            = models.CharField(max_length=255, default='', null=True, blank=True)
    entry_date      = models.CharField(max_length=255)
    entry_time      = models.CharField(max_length=255)
    is_active       = models.BooleanField(default=True)
    is_deleted      = models.BooleanField(default=False)
    updated_at      = models.DateTimeField(auto_now=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.rtqm_dt_no} [ {self.rtqm_no} ]"
    
    class Meta:
        db_table = 'rtqm_defect_dt'
        app_label = 'QMS_db'
    