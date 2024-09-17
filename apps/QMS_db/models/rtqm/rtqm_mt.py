from django.db import models
from QMS_db.models import QmsPlaning


class RtqmMt(models.Model):
    rtqm_no         = models.CharField(max_length=30, unique=True)
    total_quantity  = models.IntegerField(default=0)
    planing         = models.ForeignKey(QmsPlaning,on_delete=models.CASCADE,db_constraint=False,null=True,blank=True)
    is_active       = models.BooleanField(default=True)
    is_deleted      = models.BooleanField(default=False)
    updated_at      = models.DateTimeField(auto_now=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.planing} - {self.rtqm_no} "
    
    class Meta:
        unique_together = ('rtqm_no','planing')
        db_table = 'rtqm_mt'
        app_label = 'QMS_db'
    