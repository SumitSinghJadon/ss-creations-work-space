from django.db import models


class OtApproval(models.Model):
    unit_code = models.CharField(max_length=100)
    dayno = models.DateField()

    emp_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    ot_hour = models.IntegerField()
    approve_status = models.IntegerField()
    approve_by = models.CharField(max_length=100,blank = True,null = True)
    approve_date = models.CharField(max_length=100,blank = True,null = True)
    gm_approve_by = models.CharField(max_length=100,blank = True,null = True)
    gm_approve_date = models.CharField(max_length=100,blank = True,null = True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auto_no = models.IntegerField(default=False)
    
    def __str__(self):
        return self.dayno
    
    class Meta:
        db_table ='ot_approval'
    
    