from django.db import models
from IntelliSync_db.models import LocationMaster


class MeetingRoomMaster(models.Model):
    location = models.ForeignKey(LocationMaster, on_delete=models.DO_NOTHING, db_constraint=False, db_column='location', blank=True, null=True)
    room_name = models.CharField(max_length=100, blank=True, null=True)
    Remarks = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meeting_room_master'
        app_label = 'HRMS_db'