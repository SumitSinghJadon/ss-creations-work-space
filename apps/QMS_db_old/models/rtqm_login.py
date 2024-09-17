from django.db import models
from IntelliSync_db.models import LocationMaster ,CommonMaster,FirstLevelMaster 



class RTQMLogin(models.Model):
    line = models.ForeignKey(FirstLevelMaster,on_delete=models.CASCADE ,db_constraint=False)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        db_table = 'rtqm_login'
        app_label = 'QMS_db'
        
    def __str__(self):
        return self.styleno
