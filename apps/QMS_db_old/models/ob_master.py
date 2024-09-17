from django.db import models
from IntelliSync_db.models import User


class ObMaster(models.Model):
    buyer_code = models.CharField(max_length=255, default='', null=True, blank=True)
    buyer_name = models.CharField(max_length=255, default='', null=True, blank=True)
    style      = models.CharField(max_length=255, default='', null=True, blank=True)
    line_sum   = models.FloatField(null=True, blank=True)
    ob_no      = models.CharField(max_length=255, default='', null=True, blank=True)
    ob_date    = models.DateField(null=True, blank=True)
    line_sam   = models.FloatField(null=True, blank=True)
    re_cutting = models.CharField(max_length=255, default='', null=True, blank=True)
    kaz_button = models.CharField(max_length=255, default='', null=True, blank=True)
    other      = models.CharField(max_length=255, default='', null=True, blank=True)
    total_sam  = models.FloatField(null=True, blank=True)
    is_active  = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False)
    ourref     = models.CharField(max_length=255, default='', null=True, blank=True)
    color      = models.CharField(max_length=255, default='', null=True, blank=True)
    
    def __str__(self):
        return f"{self.buyer_name} [ {self.style} ]"
    
    class Meta:
        db_table = 'ob_master'
        app_label = 'QMS_db'
    


class ObDetail(models.Model):
    ob_mt                  = models.ForeignKey(ObMaster, on_delete=models.CASCADE, db_constraint=False,null=True, blank=True)
    ob_no                  = models.CharField(max_length=255, default='', null=True, blank=True)
    parts                  = models.CharField(max_length=100, null=True, blank=True)
    operation              = models.CharField(max_length=1500, null=True, blank=True)
    type_of_machine        = models.CharField(max_length=1500, null=True, blank=True)
    attachments            = models.CharField(max_length=1500, null=True, blank=True)
    sam                    = models.FloatField(null=True, blank=True)
    theoretical_manpower   = models.FloatField(null=True, blank=True)
    planned_work_station   = models.IntegerField(null=True, blank=True)
    target_100_pcs         = models.IntegerField(null=True, blank=True)
    target_60_pcs          = models.IntegerField(null=True, blank=True)
    seam_length            = models.IntegerField(null=True, blank=True)
    remark                 = models.CharField(max_length=1500, null=True,blank=True) 
    
    # operation_sam          = models.FloatField(null=True, blank=True)
    # balanced_manpower      = models.FloatField(null=True, blank=True)
    # actual_manpower        = models.FloatField(null=True, blank=True)

    is_active  = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.parts

    class Meta:
        db_table = 'ob_detail'
        app_label = 'QMS_db'