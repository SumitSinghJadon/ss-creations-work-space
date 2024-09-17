from django.db import models
from .order_mt import OrderMt


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