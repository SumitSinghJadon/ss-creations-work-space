from django.db import models


class MmrMT(models.Model):
    mmr_code = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auto_no = models.IntegerField(default=False)
    
    created_by =models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)

    def __str__(self):
        return self.mmr_code
    
    class Meta:
        db_table ='mmr_mt'
        app_label = 'App_db'
    
    