from django.db import models
# from database.models import *
from ERP_db.models.part import Party
from IntelliSync_db.models.location_master import LocationMaster

class ProdProcPlanMt(models.Model):
    plan_no = models.CharField(max_length=100)
    # detail_type = models.CharField(max_length =100)
    # buyer_code = models.ForeignKey(Party,on_delete=models.DO_NOTHING,db_column='party_code',db_constraint=False)
    buyer_code = models.CharField(max_length =100)
    style_no = models.CharField(max_length =100)
    order_no = models.CharField(null=True,blank=True,max_length =100)
    color = models.CharField(max_length=100,blank=True, null=True)
    u_id = models.ForeignKey(LocationMaster,on_delete=models.DO_NOTHING,db_constraint=False)
    entry_date = models.DateField()
    # Defalut Fields
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.plan_no

    class Meta:
        db_table = 'prod_proc_plan_mt'
        app_label = 'IS_erp_db'