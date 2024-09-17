from django.db import models
from IS_erp_db.models import ProdProcPlanMt
from IntelliSync_db.models import CommonMaster
from IntelliSync_db.models import FirstLevelMaster,SecondLevelMaster

class ProdProcPlanDt(models.Model):
    mt = models.ForeignKey(ProdProcPlanMt,on_delete=models.CASCADE,db_constraint=False)
    plan_no = models.CharField(max_length=100)
    process = models.ForeignKey(FirstLevelMaster,on_delete=models.CASCADE,related_name='prod_proc_process',db_constraint=False)
    product_type = models.ForeignKey(CommonMaster,on_delete=models.CASCADE,db_column='product_type',db_constraint=False)
    component = models.ForeignKey(FirstLevelMaster,on_delete=models.CASCADE,db_column='component',db_constraint=False)
    sub_component = models.ForeignKey(SecondLevelMaster,on_delete=models.CASCADE,db_column='sub_component',blank=True, null=True,db_constraint=False)
    process_no = models.IntegerField()
    process_rate = models.FloatField(default=0,null=True,blank=True)
    product_rate = models.FloatField(default=0,null=True,blank=True)
    entry_status = models.BooleanField(default=0)
    # Defalut Fields
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prod_proc_plan_dt'
        app_label = 'IS_erp_db'