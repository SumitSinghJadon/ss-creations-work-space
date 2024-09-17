from django.db import models
from IntelliSync_db.models import LocationMaster
class FileHandOver(models.Model):
    buyer = models.CharField(max_length=100)
    style = models.CharField(max_length=50)
    ourr_ef = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    order_date = models.DateField()
    delv_date = models.DateTimeField()
    order_qty= models.IntegerField()
    pcd_status = models.CharField(max_length=50)
    reason_notmeet = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=100)
    plan_qty = models.IntegerField( null=True, blank=True)
    handover_date = models.DateTimeField( null=True, blank=True)
    unit = models.ForeignKey(LocationMaster, null=True, blank=True, on_delete=models.SET_NULL, db_constraint=False)
    ppc_comment = models.CharField(max_length=100, null=True, blank=True)
    delivery_status = models.CharField(max_length=100, null=True, blank=True)
    risk_category = models.CharField(max_length=100, null=True, blank=True)
    ppm_date = models.DateTimeField(null=True, blank=True)
    rnd_comp_date = models.DateTimeField(null=True, blank=True)
    factory_comment = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by =models.CharField(max_length = 100, null=True, blank= True)
    class Meta:
        db_table = 'file_handover_mt'
        app_label = 'App_db'