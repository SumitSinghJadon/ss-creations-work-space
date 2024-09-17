from django.db import models
from App_db.models import TnaTemplateMt

class TnaEntryMt(models.Model):
    tna_entry_no    = models.CharField(max_length=30)
    buyer_code      = models.CharField(max_length=100)
    buyer_name      = models.CharField(max_length=255)
    style           = models.CharField(max_length=255)
    ref_no          = models.CharField(max_length=255)
    delivery_date   = models.DateField()
    order_date      = models.DateField()
    pcd_date        = models.DateField()
    lead_time       = models.IntegerField()
    tna_template    = models.ForeignKey(TnaTemplateMt, on_delete=models.CASCADE, db_constraint=False)
    tna_entry_date  = models.DateField()

    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = 'tna_entry_mt'
        app_label = 'App_db'

    def __str__(self):
        return self.buyer
    

class TnaEntryDt(models.Model):
    tna_mt                 = models.ForeignKey(TnaEntryMt, on_delete=models.CASCADE, db_constraint=False)
    activity               = models.CharField(max_length=255)
    base_activity          = models.CharField(max_length=255, null=True , blank= True)
    days_req               = models.IntegerField()
    days_before_after      = models.IntegerField()
    running_days           = models.IntegerField()
    days_action            = models.CharField(max_length=255)
    plan_date_start        = models.DateField()
    plan_date_end          = models.DateField()
    plan_week_day          = models.CharField(max_length=255, null=True, blank=True)
    res_person             = models.CharField(max_length=255)
    res_department         = models.CharField(max_length=255)
    remark                 = models.CharField(max_length=255, null=True, blank=True)

    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  =  'tna_entry_dt'
        app_label =  'App_db'

    def __str__(self):
        return self.base_activity   
    


