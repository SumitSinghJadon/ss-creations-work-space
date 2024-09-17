from django.db import models
# from App_db.models import SampleBookingMt
from IntelliSync_db.models import CommonMaster


class CheckerStatusMt(models.Model):
    checker_status = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='csm_checker_status', db_constraint=False)
    deliver_loss_time = models.DateTimeField()
    remarks = models.TextField(max_length = 100, null=True, blank=True)
    returned_date = models.DateTimeField()
    hold_reason = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='csm_hold_reason', db_constraint=False)
    delay_reason = models.ForeignKey(CommonMaster, on_delete=models.CASCADE, related_name='csm_delay_reason', db_constraint=False)
    qa_remarks = models.TextField(max_length = 100, null=True, blank= True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'check_status_mt'
        app_label = 'App_db'

    def __str__(self):
        return self.checker_status

