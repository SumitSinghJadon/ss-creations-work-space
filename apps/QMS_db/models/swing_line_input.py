# from django.db import models
# from IntelliSync_db.models.common_master import CommonMaster, FirstLevelMaster
# from IntelliSync_db.models.location_master import LocationMaster
# from QMS_db.models import QmsPlaning
# class SwingLineInputMt(models.Model):
#     planing = models.ForeignKey(QmsPlaning,on_delete=models.CASCADE,db_constraint=False,null=True,blank=True)
#     total_input_qty = models.IntegerField(default=0,blank=True,null=True)
#     is_active = models.BooleanField(default=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         # unique_together = ('buyer','style_no')
#         app_label = 'QMS_db'
#         db_table = 'swing_line_input_mt'
        
    
#     def __str__(self):
#         return f" {self.planing}"


# class SwingLineInputDt(models.Model):
#     mt_id = models.ForeignKey(SwingLineInputMt, on_delete=models.CASCADE,db_constraint=False)
#     quantity = models.IntegerField(default=0)
#     size   = models.CharField(max_length=40)
#     is_active = models.BooleanField(default=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         app_label = 'QMS_db'
#         db_table = 'swing_line_input_dt'
        
#     def __str__(self):
#         return f" {self.mt_id} - {self.size} - {self.quantity}"


from django.db import models
from QMS_db.models import QmsPlaning

class SewingLineInputMt(models.Model):
    planing             = models.ForeignKey(QmsPlaning, on_delete=models.CASCADE, db_constraint=False, null=True, blank=True)
    total_input_qty     = models.IntegerField(default=0)
    size                = models.CharField(max_length=40)
    is_active           = models.BooleanField(default=True)
    updated_at          = models.DateTimeField(auto_now=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'QMS_db'
        db_table = 'sewing_line_input_mt'
    def __str__(self):
        return f" {self.planing}"
    
class SewingLineInputDt(models.Model):
    mt_id       = models.ForeignKey(SewingLineInputMt, on_delete=models.CASCADE,db_constraint=False)
    input_qty   = models.IntegerField(default=0)
    entry_date  = models.CharField(max_length=255)
    entry_time  = models.CharField(max_length=255)
    is_active   = models.BooleanField(default=True)
    updated_at  = models.DateTimeField(auto_now=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'QMS_db'
        db_table = 'sewing_line_input_dt'
    def __str__(self):
        return f" {self.mt_id} - {self.mt_id.size} - {self.input_qty}"