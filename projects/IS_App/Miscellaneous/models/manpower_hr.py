from django.db import models


class ManpowerHrMt(models.Model):
    dayno = models.DateField(null=True,blank=True)
    mmr_code = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=100)
    onroll = models.IntegerField(default=True)
    manpower = models.IntegerField(default=True)
    remarks = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.dept
    
    class Meta:
        db_table ='manpower_hr'
    
    