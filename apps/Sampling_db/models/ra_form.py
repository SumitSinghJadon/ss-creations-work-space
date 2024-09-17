from django.db import models
from IntelliSync_db.models import CommonMaster, User, FirstLevelMaster


class RaFormMt(models.Model):
    style_risk_category_choices=(
        ('H','High'),
        ('M','Medium'),
        ('L','Low'),
    )
    ra_no        = models.CharField(max_length=30)
    ra_date= models.DateTimeField(null=True, blank=True)
    style_no= models.CharField(max_length=200, null=True, blank=True)
    buyer= models.CharField(max_length=200, null=True, blank=True)
    product_type= models.CharField(max_length=100, null=True, blank=True)
    buyer_department= models.CharField(max_length=200, null=True, blank=True)
    po_number= models.CharField(max_length=200, null=True, blank=True)
    erp_order= models.CharField(max_length=200, null=True, blank=True)
    order_qty= models.CharField(max_length=200, null=True, blank=True)
    remarks= models.TextField(null=True, blank=True)
    style_risk_category= models.CharField(max_length=20, choices=style_risk_category_choices,null=True,blank=True)
    area_of_risk= models.TextField(null=True, blank=True)
    picture_of_style=models.ImageField(upload_to='ra_booking/', null=True, blank=True)
    merchant_head     = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='ra_merchant_head', db_constraint=False,null=True,blank=True)
    merchant_name     = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='ra_merchant_name', db_constraint=False,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False,related_name="ra_status_mt_created_by")
    is_active  = models.BooleanField(default=True)  # Closed
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by=models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False,null=True,blank=True,related_name="ra_status_mt_updated_by")

    delivery_date= models.CharField(max_length=200, null=True, blank=True)
    shell= models.TextField(null=True, blank=True)
    trim=models.TextField(null=True, blank=True)

    class Meta:
        db_table    = 'ra_status_mt'
        app_label   = 'Sampling_db'
        # unique_together = ('booking_no', 'size', 'color')

    def __str__(self):
        return self.ra_no


class RaFormDt(models.Model):
    ra_no = models.CharField(max_length=30)
    mt_id = models.ForeignKey(RaFormMt, on_delete=models.DO_NOTHING,db_constraint=False, related_name='ra_form_dt_ra_no')
    category= models.ForeignKey(CommonMaster, on_delete=models.DO_NOTHING, db_constraint=False, related_name='ra_form_dt_category')
    category_content= models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False,related_name="ra_form_dt_category_content")
    is_active  = models.BooleanField(default=True) 
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by=models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False,null=True,blank=True)
    # category_index= models.FloatField(null=True, blank=True)

    

    class Meta:
        db_table = 'ra_form_dt'
        app_label = 'Sampling_db'

    def __str__(self):
        return self.ra_no

