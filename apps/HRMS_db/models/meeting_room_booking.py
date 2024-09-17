from django.db import models
from IntelliSync_db.models import LocationMaster,User
from Payroll_db.models import EmployeeMaster
from .meeting_room_master import MeetingRoomMaster


class MeetingRoomBooking(models.Model):

    meeting_type_list = (
        ('IN', 'Internal'),
        ('EX', 'External'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meeting_room_user', db_constraint=False, null=True, blank=True)
    meeting_date = models.DateField(null=True,blank=True)
    meeting_type = models.CharField(max_length=100,null=True,blank=True,choices=meeting_type_list)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    purpose = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    location = models.ForeignKey(LocationMaster, on_delete=models.DO_NOTHING, db_constraint=False, db_column='location',blank=True, null=True)
    room_name = models.ForeignKey(MeetingRoomMaster, on_delete=models.DO_NOTHING, db_constraint=False, db_column='room_name',blank=True, null=True)
    guest_name = models.CharField(max_length=100,null=True,blank=True)
    no_of_attendees = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meeting_room_booking'
        app_label = 'HRMS_db'
