from django.db import models
from IntelliSync_db.models import CommonMaster
# from Sampling_db.models import SampleBookingMt


class DispatchEntryMt(models.Model):
    dispatch_dt = models.ForeignKey('dispatchTransactionDt', on_delete=models.CASCADE, db_column='dispatch_dt', null=True, blank=True, db_constraint=False,)
    booking_no = models.CharField(max_length=100, default='')
    booking_id = models.ForeignKey('SampleBookingMt', on_delete=models.CASCADE, related_name='dem_booking_no', db_constraint=False, db_column='booking_id')
    qty = models.PositiveBigIntegerField(null=True, blank= True)
    size = models.CharField(max_length = 100, null=True, blank= True)
    color = models.CharField(max_length = 100, null=True, blank= True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)
    class Meta:
        db_table = 'dispatch_entry_dt'
        app_label = 'Sampling_db'
        # unique_together = ('booking_no', 'size', 'color')

    def __str__(self):
        return self.sample_type


class DispatchTransactionDt(models.Model):
    booking_no = models.CharField(max_length=100, default='')
    booking_id = models.ForeignKey('SampleBookingMt', on_delete=models.CASCADE, db_constraint=False, db_column='booking_id')
    transaction_no = models.TextField(max_length = 100, null=True, blank= True)
    dispatch_type = models.TextField(max_length = 100, null=True, blank= True)
    dispatch_qty = models.TextField(max_length = 100, null=True, blank= True)
    size_breakup = models.TextField(max_length = 100, null=True, blank= True)
    remarks = models.TextField(max_length = 100, null=True, blank= True)
    handover_to = models.TextField(max_length = 100, null=True, blank= True)
    delay_reason = models.TextField(max_length = 100, null=True, blank= True)
    sample_dept = models.TextField(max_length = 100, null=True, blank= True)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length = 100, null=True, blank= True)
    created_at = models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)
    updated_at = models.CharField(max_length = 100, null=True, blank= True)

    class Meta:
        db_table = 'dispatch_entry_mt'
        app_label = 'Sampling_db'

    def __str__(self):
        return self.dispatch_type    


