from django.db import models
from .user_master import User


class StatusTrackerMaster(models.Model):
    page_code_list=(
        ('MPR','Manpower Requisition'),
    )

    status_list=(
        ('P','Pending'),
        ('AHOD','Approved by HOD'),
        ('RHOD','Rejected by HOD'),
        ('AM','Approved by Management'),
        ('RM','Rejected by Management')
    )

    page=models.CharField(max_length=10,choices=page_code_list)
    application_id=models.BigIntegerField()
    status=models.CharField(max_length=10,choices=status_list)
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_constraint='False')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'status_tracker_master'
        app_label='IntelliSync_db'
        unique_together = ('page', 'application_id','status')