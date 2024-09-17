from django.db import models


class ProcessMaster(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'process_master'
        app_label = 'QMS_db'


class DefectMaster(models.Model):
    CATEGORY_CHOICES = (
        ('MINOR', 'MINOR'),
        ('MAJOR', 'MAJOR')
    )

    name       =  models.CharField(max_length=255, default='', null=True, blank=True)
    hindi_name =  models.CharField(max_length=255, default='', null=True, blank=True)
    process    = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE, db_constraint=False , null=True, blank=True ) 
    remarks    = models.CharField(max_length=255 ,default='')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)
    is_active  = models.BooleanField(default=True)
    is_reject  = models.BooleanField(default=False)
    critical   = models.CharField(max_length=50,blank=True,null=True,choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return f"{self.name} [ {self.status} ]"
    
    class Meta:
        db_table = 'defect_master'
        app_label = 'QMS_db'
        
