from django.db import models


class OrderMt(models.Model):
    buyer = models.CharField(max_length=100, blank=True, null=True)
    buyer_order_no=models.CharField(max_length=20,blank=True, null=True)
    ourref_no = models.CharField(max_length=100,blank=True, null=True)
    style_no = models.CharField(max_length=100,blank=True, null=True)
    delivery_date = models.DateField(auto_now=False, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    color  = models.CharField(max_length=100,blank=True, null=True)
    style_name = models.CharField(max_length=100, blank=True, null=True)
    Style_category = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        unique_together = ('ourref_no','style_no','color')
        app_label = 'QMS_db'
        db_table = 'order_mt'

    def __str__(self):
        return self.ourref_no 
