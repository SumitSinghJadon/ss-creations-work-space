from django.db import models
from IntelliSync_db.models import User


class LeaveApplication(models.Model):
    day_part_list = (
        ('FD', 'Full Day'),
        ('HD', 'Half Day'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_application_user', db_constraint=False)
    dep = models.CharField(max_length=100, blank=True, null=True)
    application_type = models.CharField(max_length=100, blank=True, null=True)
    leave_type = models.CharField(max_length=100, blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    till_date = models.DateTimeField(blank=True, null=True)
    time = models.CharField(max_length=20, null=True)
    working_day = models.CharField(max_length=100, blank=True, null=True)
    day_part = models.CharField(max_length=20, blank=True, null=True, choices=day_part_list)
    day_count = models.CharField(max_length=100, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    visit_location_type = models.CharField(max_length=300, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=300, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='applications/', blank=True, null=True)
    updated_by=models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False,db_column='updated_by',related_name='leave_application_updated_by',blank=True,null=True)
    applied_on = models.DateTimeField(blank=True, null=True)
    approved_on = models.DateTimeField(blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed=False
        db_table = 'application'
        app_label='HRMS_db'
