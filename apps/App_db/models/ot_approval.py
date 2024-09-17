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
    auto_no = models.IntegerField(default=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by =models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)

    def __str__(self):
        return self.dayno
    
    class Meta:
        db_table ='ot_approval'
        app_label = 'App_db'
    
    