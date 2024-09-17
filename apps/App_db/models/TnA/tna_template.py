from django.db import models
from IntelliSync_db.models import CommonMaster, FirstLevelMaster


class TnaTemplateMt(models.Model):
    template_no    = models.CharField(max_length=30)
    template_name  = models.CharField(max_length=255)
    template_desc  = models.CharField(max_length=255)
    buyer_name     = models.CharField(max_length =100)
    buyer_code     = models.CharField(max_length =100)
    days_from      = models.IntegerField()
    days_to        = models.IntegerField()
    status         = models.CharField(max_length=30, default='pending')

    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = 'tna_template_mt'
        app_label = 'App_db'

    def __str__(self):
        return self.template_name



class TnaTemplateDt(models.Model):
    tna_mt         = models.ForeignKey(TnaTemplateMt, on_delete=models.CASCADE, db_constraint=False)
    seq_no         = models.IntegerField()
    activity_group = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='tna_template_dt_group', db_constraint=False)
    activity_name  = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='tna_template_dt_name', db_constraint=False)
    activity_type  = models.CharField(max_length=30)
    days_action       = models.CharField(max_length=30)
    days_req          = models.IntegerField()
    days_after_before = models.IntegerField(blank=True, null= True)
    running_days      = models.IntegerField(blank=True, null=True)
    base_activity     = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='tna_template_dt_activity', null=True, blank=True, db_constraint=False)
    status            = models.CharField(max_length=30)

    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = 'tna_template_dt'
        app_label = 'App_db'

    def __str__(self):
        return self.tna_mt
    

