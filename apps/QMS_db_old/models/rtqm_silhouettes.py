from django.db import models
from datetime import datetime
from django.utils import timezone
from django.db.models import JSONField 


class RTQMDateID(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 50
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        today = timezone.now().date()
        value = f'rtqm_{today.isoformat()}'
        setattr(model_instance, self.attname, value)
        return value


class RTQMSilhouettes(models.Model):
    id = RTQMDateID(primary_key=True, editable=False)
    buyer = models.CharField(max_length=100)
    ourref = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    defect_operation = JSONField(default=list)  
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"DefectOperationData {self.id}"
    
    class Meta:
        db_table = 'rtqm_silhouettes'
        app_label = 'QMS_db'
