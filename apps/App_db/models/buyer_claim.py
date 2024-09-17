from django.db import models 
 
class BuyerClaimModel(models.Model):
    CLAIM_TYPE = [
        ('Buyer Claim', 'Buyer Claim'),
        ('Discount', 'Discount'),
        ('Intimation', 'Intimation')
    ]

    financial_year = models.CharField(max_length=9)  
    loss_type = models.CharField(max_length=50, choices=CLAIM_TYPE)
    loss_date = models.DateField()
    invoice_no = models.CharField(max_length=20)
    buyer = models.CharField(max_length=100)  
    style = models.CharField(max_length=50)  
    unit_name = models.CharField(max_length=100)  
    amount_fc =  models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency = models.CharField(max_length=5)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    debit_note_amount = models.DecimalField(max_digits=15,decimal_places=2)
    debit_no = models.CharField(max_length=20, unique=True)
    reason = models.CharField(max_length=100)   
    remarks = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by =models.CharField(max_length = 100, null=True, blank= True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)

    def __str__(self):
        return f"{self.loss_type} - {self.invoice_no} - {self.amount} {self.currency}"
    class Meta():
        app_label = 'App_db'
        db_table ='buyer_claim'