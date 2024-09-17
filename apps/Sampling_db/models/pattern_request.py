# from django import forms
# from django.db import models

# from IntelliSync_db.models.common_master import CommonMaster, FirstLevelMaster


# class PatternRequestMt(models.Model):


#     request_type_choices=(
#         ('F','Fresh'),
#         ('C','Correction'),
#         ('c','Consumption')
#     )
#     REQUIREMENTS_CHOICES = [
#     ('PATTERN', 'PATTERN'),
#     ('PLOT', 'PLOT'),
#     ]
    
#     request_no = models.CharField(max_length=30)

#     # transaction_date  = models.DateTimeField()

#     request_date = models.DateField(null=True, blank=True)

#     request_type = models.CharField(max_length=10,choices=request_type_choices)

#     # pattern_stage = models.TextField(max_length=255, null=True, blank=True)

#     pattern_stage =  models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='pattern_request_pattern_stage', db_constraint=False)


#     # pattern_type = models.TextField(max_length=255, null=True, blank=True)

#     pattern_type =models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='pattern_request_pattern_type', db_constraint=False)

#     buyer_name = models.CharField(max_length=255, null=True, blank=True)

#     style_name = models.CharField(max_length=100, null=True, blank=True) 

#     color_name = models.CharField(max_length=100, null=True, blank=True)


#     merchant_head     = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='pattern_request_merchant_head', db_constraint=False)

#     merchant     = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='pattern_request_merchant_name', db_constraint=False)
#     target_date       = models.DateTimeField(null=True)

#     pattern_master = models.CharField(max_length=100, null=True, blank=True)

#     # requirements = models.CharField(max_length=100, null=True, blank=True)

#     requirement = forms.MultipleChoiceField(choices=REQUIREMENTS_CHOICES,
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )


#     no_of_pattern_develop = models.CharField(max_length=100, null=True, blank=True)
    
#     remarks           = models.TextField(null=True, blank=True)

#     # expected_del_date = models.DateField(null=True, blank=True)
#     # expected_del_time = models.TimeField(null=True, blank=True)

#     is_active  = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.CharField(max_length = 100, null=True, blank= True)
    
#     class Meta:
#         db_table = 'pattern_request_mt'
#         app_label = 'Sampling_db'


from django import forms
from django.db import models

from IntelliSync_db.models.common_master import CommonMaster, FirstLevelMaster


class PatternRequestMt(models.Model):


    request_type_choices=(
        ('F','Fresh'),
        ('C','Correction'),
        ('S','Consumption')
    )
    pattern_type_choices=(
        ('D','Done'),
        ('H','Hold'),
        ('C','Cancel'),
        
    )
    plot_choices=(
        ('d','Done'),
        ('h','Hold'),
        ('c','Cancel'),
    )
    
    request_no = models.CharField(max_length=30)
    request_date = models.DateTimeField(null=True)
    request_type = models.CharField(max_length=10,choices=request_type_choices)
    # pattern_stage = models.TextField(max_length=255, null=True, blank=True)
    pattern_stage =  models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='pattern_request_pattern_stage', db_constraint=False)
    # pattern_type = models.TextField(max_length=255, null=True, blank=True)
    pattern_type =models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='pattern_request_pattern_type', db_constraint=False)
    buyer_name = models.CharField(max_length=255, null=True, blank=True)
    style_name = models.CharField(max_length=100, null=True, blank=True) 
    color_name = models.CharField(max_length=100, null=True, blank=True)
    buyer_code=models.CharField(max_length=100,null=True,blank=True)
    merchant_head = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='pattern_request_merchant_head', db_constraint=False)
    merchant = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE, related_name='pattern_request_merchant_name', db_constraint=False)
    target_date = models.DateTimeField(null=True)
    pattern_master = models.CharField(max_length=100, null=True, blank=True)

    requirements = models.CharField(max_length=100, null=True, blank=True)

    # requirement = forms.MultipleChoiceField(choices=REQUIREMENTS_CHOICES,
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )
    attachment=models.ImageField(upload_to='pattern_request/',null=True,blank=True)
    pattern_attachment=models.ImageField(upload_to='pattern_request/',null=True,blank=True)


    no_of_pattern_develop = models.CharField(max_length=100, null=True, blank=True)
    
    remarks           = models.TextField(null=True, blank=True)

    # expected_del_date = models.DateField(null=True, blank=True)
    # expected_del_time = models.TimeField(null=True, blank=True)

    is_active  = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length = 100, null=True, blank= True)

    pattern_done = models.CharField(max_length=10,choices=pattern_type_choices,null=True,blank=True)
    plot_done = models.CharField(max_length=10,choices=plot_choices,null=True,blank=True)
    pattern_cmd_date_and_time = models.DateTimeField(null=True)

    upload_by = models.CharField(max_length = 100, null=True, blank= True)
    plot_by_done = models.CharField(max_length = 100, null=True, blank= True)
    plot_date_and_time = models.DateTimeField(null=True)
    pattern_value = models.CharField(max_length = 100, null=True, blank= True)
    pattern_master_remarks=models.CharField(max_length = 100, null=True, blank= True)
    
    class Meta:
        db_table = 'pattern_request_mt'
        app_label = 'Sampling_db'



