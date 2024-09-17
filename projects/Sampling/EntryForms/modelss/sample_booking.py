from django.db import models
from IntelliSync_db.models import CommonMaster, CommonMasterType, User, FirstLevelMaster
# from IntelliSync.database import  


class SampleBookingMt(models.Model):
    booking_no    = models.CharField(max_length=30)
    image1        = models.ImageField(upload_to='sample booking/')
    image2        = models.ImageField(upload_to='sample booking/', null=True, blank=True)
    booking_type  = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_booking_type', db_constraint=False)
    merchant_head = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_merchant_head', db_constraint=False)
    merchant_name = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='sbm_merchant_name', db_constraint=False)
    # buyer         = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_buyer', db_constraint=False)
    buyer_code    = models.CharField(max_length=30, null=True, blank=True)  
    buyer_name    = models.CharField(max_length=30, null=True, blank=True)  
    sample_type   = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_sample_type', db_constraint=False)
    style_no      = models.CharField(max_length=30, null=True, blank=True) 
    season        = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_season', db_constraint=False)
    season_year   = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_year', db_constraint=False)
    product_type  = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_product_type', db_constraint=False)
    booking_date  = models.DateTimeField()
    target_date   = models.DateTimeField()
    remarks = models.TextField(null=True, blank=True)
    booking_status = models.CharField(max_length=64)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sample_booking_mt'
        app_label = 'App_db'

    def __str__(self):
        return self.booking_no


class SampleArticleDetails(models.Model):
    booking_id        = models.ForeignKey(SampleBookingMt, on_delete=models.CASCADE)
    booking_no        = models.CharField(max_length=30)
    given_by_merchant = models.CharField(max_length=30)
    article_name      = models.CharField(max_length=100)
    comment           = models.CharField(max_length=100, null=True, blank=True)
    expected_date     = models.DateTimeField(null=True, blank=True)

    is_active   = models.BooleanField(default=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sample_article_details'
        app_label = 'App_db'

    def __str__(self):
        return self.booking_no
    
    def save(self, *args, **kwargs):
        # Save booking no automatically at the time of object creation
        self.booking_no = self.booking_id.booking_no
        super().save(*args, **kwargs)


class SampleSizeQuantity(models.Model):
    booking_id  = models.ForeignKey(SampleBookingMt, on_delete=models.CASCADE)
    booking_no  = models.CharField(max_length=30)
    size        = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_size', db_constraint=False)
    color       = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='sbm_color', db_constraint=False)
    quantity    = models.PositiveIntegerField()

    is_active   = models.BooleanField(default=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sample_size_quantity'
        app_label = 'App_db'

    def __str__(self):
        return self.booking_no

    def save(self, *args, **kwargs):
        # Save booking no automatically at the time of object creation
        self.booking_no = self.booking_id.booking_no
        super().save(*args, **kwargs)

