from django.db import models
# from App_db.models import SampleBookingMt
from IntelliSync_db.models import CommonMaster


class CuttingEntryMt(models.Model):
    cutting_transaction_dt = models.ForeignKey('CuttingTransactionDt', on_delete=models.CASCADE, db_column='cutting_transaction_dt')
    booking_no = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='cem_booking_no', db_constraint=False)
    sample_booking_type = models.DateTimeField()
    sample_type = models.TextField(max_length = 100, null=True, blank=True)
    merchant_name = models.DateTimeField()
    merchant_group_name = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='cem_merchant_group_name', db_constraint=False)
    buyer = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='cem_buyer', db_constraint=False)
    style_no = models.TextField(max_length = 100, null=True, blank= True)
    season = models.TextField(max_length = 100, null=True, blank= True)
    year = models.TextField(max_length = 100, null=True, blank= True)
    target_date = models.TextField(max_length = 100, null=True, blank= True)
    booked_date = models.TextField(max_length = 100, null=True, blank= True)
    qty = models.TextField(max_length = 100, null=True, blank= True)
    size = models.TextField(max_length = 100, null=True, blank= True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cutting_entry_mt'
        app_label = 'App_db'

    def __str__(self):
        return self.sample_type
    

class CuttingTransactionDt(models.Model):
    transaction_no = models.TextField(max_length = 100, null=True, blank= True)
    cutting_type = models.TextField(max_length = 100, null=True, blank= True)
    cut_qty = models.TextField(max_length = 100, null=True, blank= True)
    size_breakup = models.TextField(max_length = 100, null=True, blank= True)
    cutter_name = models.TextField(max_length = 100, null=True, blank= True)
    assign_date = models.TextField(max_length = 100, null=True, blank= True)
    handover_to_supervisor = models.TextField(max_length = 100, null=True, blank= True)
    remarks = models.TextField(max_length = 100, null=True, blank= True)
    sample_status = models.TextField(max_length = 100, null=True, blank= True)

    class Meta:
        db_table = 'cutting_transaction_details'
        app_label = 'App_db'

    def __str__(self):
        return self.cutting_type    


