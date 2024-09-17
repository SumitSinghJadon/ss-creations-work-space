from django.db import models
from IntelliSync_db.models import CommonMaster, User, FirstLevelMaster


class OtherTransMt(models.Model):
    booking_type_choices = (
        ('A', 'Alter'),
        ('F', 'Fresh'),
        ('R', 'Resubmission'),
    )

    image1            = models.ImageField(upload_to='other booking/')
    image2            = models.ImageField(upload_to='other booking/', null=True, blank=True)
    process_type      = models.ForeignKey(FirstLevelMaster, on_delete=models.DO_NOTHING, null=True, blank=True, db_constraint=False)
    booking_no        = models.CharField(max_length=30)
    booking_type      = models.CharField(max_length=10, choices=booking_type_choices)
    merchant_head     = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='obm_merchant_head', db_constraint=False)
    merchant_name     = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='obm_merchant_name', db_constraint=False)
    buyer_code        = models.CharField(max_length=100, null=True, blank=True) 
    buyer_name        = models.CharField(max_length=255, null=True, blank=True) 

    emp_data          = models.CharField(max_length=255, null=True, blank=True) 
    supervisor        = models.CharField(max_length=255, null=True, blank=True) 
    checker           = models.CharField(max_length=255, null=True, blank=True) 
    
    department_id      =models.CharField(max_length=255, null=True, blank=True)  
    department_name      =models.CharField(max_length=255, null=True, blank=True)  

    sample_group_type = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='obm_sample_type', db_constraint=False)
    sample_type       = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='obm_sample_type', db_constraint=False)
    style_no          = models.CharField(max_length=100, null=True, blank=True) 
    season            = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='obm_season', db_constraint=False)
    season_year       = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='obm_year', db_constraint=False)
    booking_date      = models.DateTimeField()
    
    transaction_date  = models.DateTimeField()

    target_date       = models.DateTimeField()

    product_type      = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='obm_product_type', db_constraint=False)
    remarks           = models.TextField(null=True, blank=True) 
    total_qty         = models.PositiveBigIntegerField(null=True, blank=True)
    reason            = models.TextField(null=True, blank=True)

    material_status   = models.CharField(max_length=64, default='pending')
    booking_status    = models.CharField(max_length=64, default='pending', null=True, blank=True)
    file_status       = models.CharField(max_length=64, default='', null=True, blank=True)
    file_rcv_date     = models.DateTimeField(null=True, blank=True)
    article_hold_reason    = models.TextField(null=True, blank=True)
    article_reject_reason  = models.TextField(null=True, blank=True)
    booking_hold_reason    = models.TextField(null=True, blank=True)
    booking_cancelled_reason = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    is_active  = models.BooleanField(default=True)  # Closed
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table    = 'other_booking_mt'
        app_label   = 'Sampling_db'
        # unique_together = ('booking_no', 'size', 'color')

    def __str__(self):
        return self.booking_no


class OtherSizeQuantity(models.Model):
    booking_id  = models.ForeignKey(OtherTransMt, on_delete=models.CASCADE)
    booking_no  = models.CharField(max_length=30)
    size        = models.CharField(max_length=100)
    color       = models.CharField(max_length=100)
    quantity    = models.PositiveIntegerField() 
    is_active   = models.BooleanField(default=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'other_size_quantity'
        app_label = 'Sampling_db'

    def __str__(self):
        return self.booking_no

