from django.db import models

class OrderProcess(models.Model):
    orderMT_id = models.ForeignKey('OrderMt', on_delete=models.CASCADE, blank=True, null=True)
    sequence = models.IntegerField()
    process = models.CharField(max_length=50)


    class Meta:
        app_label = 'QMS_db'
        db_table = 'order_process'

    def __str__(self):
        return self.orderMT_id.buyer     