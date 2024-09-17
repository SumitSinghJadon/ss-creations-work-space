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


class OrderDt(models.Model):
    order_mt = models.ForeignKey(OrderMt, on_delete=models.CASCADE, db_column='order_mt', blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'QMS_db'
        db_table = 'order_dt'

    def __str__(self):
        return str(self.order_mt) + ' ' + str(self.size) + ' ' + str(self.quantity)