from django.db import models
from IntelliSync_db.models import CommonMaster


class CuttingTransactionMt(models.Model):
    booking_no          = models.IntegerField(null=True, blank=True)
    sample_booking_type = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='ctm_sample_booking_type', db_constraint=False)

    class Meta:
        db_table = 'sample_transaction_mt'
        app_label = 'Sampling_db'



#     sample_type         = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbi_sample_type', db_constraint=False)
#     merchant_name       = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbi_merchant_name', db_constraint=False)
#     merchant_group_name = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbi_merchant_group_name', db_constraint=False)
#     buyer               = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbi_buyer', db_constraint=False)
#     style_no            = models.TextField()
#     qty                 = models.IntegerField()
#     size                = models.TextField()
#     target_date         = models.DateTimeField()
#     booked_date         = models.DateTimeField()
#     season              = models.DateTimeField()


#     is_active           = models.BooleanField(default=True)
#     updated_at          = models.DateTimeField(auto_now=True)
#     created_at          = models.DateTimeField(auto_now_add=True)


    
#     class Meta:
#         db_table = 'sample_transaction_mt'

#     def __str__(self):
#         return self.booking_no


# class SampleTransactionEntry

