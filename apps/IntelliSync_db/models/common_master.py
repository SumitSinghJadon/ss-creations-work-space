from django.db import models


name_code_list = (
    ('CT-1', 'Pattern Request Type'),
    ('CT-2', 'Pattern Stage Master'),
    ('CT-3', 'Pattern Type Master'),
    ('CT-4', 'Sample Type Group Master'),
    ('CT-5', '2nd lvl master test'),
    ('CT-6', 'Sample Type Master'),
    ('CT-7', 'Product Master'),
    ('CT-8', 'Process Master'),
    ('CT-9', 'Component Master'),
    ('CT-10', 'Sub Component Master'),
    ('CT-11', 'Sample Article Master'),
    ('CT-12', 'Season Master'),
    ('CT-13', 'Season Year Master'),
    ('CT-14', 'Size Master'),
    ('CT-15', 'Color Master'),
    ('CT-16', 'Defect Type Master'),
    ('CT-17', 'Defect Group Master'),
    ('CT-18', 'Defect Master'),
    ('CT-19', 'Month Master'),
    ('CT-20', 'Year Master'),
    ('CT-21', 'Sample Article Group Master'),
    ('CT-22', 'Merchant Head'),
    ('CT-23', 'Merchant'),
    ('CT-24', 'Meeting Room Master'),
    ('CT-25', 'Cutting Type'),
    ('CT-26', 'Activity Group Master'),
    ('CT-27', 'Activity Master'),
    ('CT-28', 'Other')
    # ('CT-29', 'Other')
)

non_editable_list = ['CT-2', 'CT-4', 'CT-5']
first_level_list = ['CT-3', 'CT-6', 'CT-9', 'CT-11', 'CT-13', 'CT-17', 'CT-23']
second_level_list = ['CT-5', 'CT-10', 'CT-18']

class CommonMasterType(models.Model):
    label_type_master = (
        ('0', 'Common Master'),
        ('1', 'First Level Master'),
        ('2', 'Second Level Master')
    )
    
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    label_type = models.CharField(max_length=100, default='0', choices=label_type_master)
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    code = models.CharField(max_length=50, default='', null=True, blank=True, unique=True)
    editable = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'common_master_type'
        app_label = 'IntelliSync_db'
        ordering = ['parent__name']

    def __str__(self):
        return self.name


class CommonMaster(models.Model): # Base-Master
    master_type = models.ForeignKey(CommonMasterType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=50, default='', null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    other = models.CharField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'common_master'
        app_label = 'IntelliSync_db'
        unique_together = ('master_type', 'name')
    
    def save(self, *args, **kwargs):
        self.code = 'CM'+str(self.pk)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.name
    
    def get_month_list():
        return CommonMaster.objects.filter(master_type__code='CT-19').annotate(value_as_int=models.functions.Cast('value', models.IntegerField())).order_by('value_as_int').values('name', 'value')


class FirstLevelMaster(models.Model):
    common_master_type = models.ForeignKey(CommonMasterType, on_delete=models.CASCADE)
    common_master = models.ForeignKey(CommonMaster, on_delete=models.CASCADE)
    master_type = models.ForeignKey(CommonMasterType, on_delete=models.CASCADE, related_name='flm_master_type')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=50, default='', null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'first_level_master'
        app_label = 'IntelliSync_db'
        unique_together = ('common_master', 'master_type', 'name')
    
    def save(self, *args, **kwargs):
        self.code = 'FM'+str(self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SecondLevelMaster(models.Model):
    common_master_type = models.ForeignKey(CommonMasterType, on_delete=models.CASCADE, related_name='flm_common_master_type')
    common_master = models.ForeignKey(CommonMaster, on_delete=models.CASCADE)
    first_level_master = models.ForeignKey(FirstLevelMaster, on_delete=models.CASCADE)
    master_type = models.ForeignKey(CommonMasterType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=50, default='', null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'second_level_master'
        app_label = 'IntelliSync_db'
        unique_together = ('common_master','first_level_master','master_type', 'name')
    
    def save(self, *args, **kwargs):
        self.code = 'SM'+str(self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

