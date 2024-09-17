from django.db import models

class FinishEntrySizeDt(models.Model):
    # id = models.BigAutoField()
    qty = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    defect = models.CharField(max_length=100, blank=True, null=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    defect_count = models.IntegerField(blank=True, null=True)
    trans_id = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    qid = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)

    rectify_status=models.CharField(max_length=100, blank=True, null=True)
    rectify_by=models.CharField(max_length=100, blank=True, null=True)
    rectify_date=models.DateTimeField(max_length=100, blank=True, null=True)
    remarks=models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        db_table = 'finish_entry_size_dt'
        app_label = 'Sampling_db'
