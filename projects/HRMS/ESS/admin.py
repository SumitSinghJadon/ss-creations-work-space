from django.contrib import admin
from HRMS_db.models import LeaveApplication


class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'application_type', 'status', 'dep', 'approved_on', 'cancelled_on']

admin.site.register(LeaveApplication, LeaveApplicationAdmin)