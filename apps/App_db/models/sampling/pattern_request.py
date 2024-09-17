from django.db import models


class PatternRequestMt(models.Model):
    request_no = models.CharField(max_length=100)
    request_date = models.DateField(null=True, blank=True)
    request_type = models.TextField(max_length=255, null=True, blank=True)
    pattern_stage = models.TextField(max_length=255, null=True, blank=True)
    pattern_type = models.TextField(max_length=255, null=True, blank=True)
    merchant = models.TextField(max_length=255, null=True, blank=True)
    buyer_name = models.TextField(max_length=255, null=True, blank=True)
    style_name = models.TextField(max_length=255, null=True, blank=True)
    color_name = models.TextField(max_length=255, null=True, blank=True)
    pattern_master = models.TextField(max_length=255, null=True, blank=True)
    expected_del_date = models.DateField(null=True, blank=True)
    expected_del_time = models.TimeField(null=True, blank=True)

    is_active  = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pattern_request_mt'
        app_label = 'App_db'

    def __str__(self):
        return self.request_date