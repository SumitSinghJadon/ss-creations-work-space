from django.contrib import admin
from Task.models import *


class TaskMasterMtAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_active']
    list_editable = ['status']


admin.site.register(TaskMasterMt, TaskMasterMtAdmin)
admin.site.register(TaskForwardMt)
