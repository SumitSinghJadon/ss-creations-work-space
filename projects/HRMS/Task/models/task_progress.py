from django.db import models
from Task.models import TaskMasterMt


class TaskProgressMt(models.Model):
    task = models.ForeignKey(TaskMasterMt, on_delete=models.CASCADE)
    progress = models.IntegerField()
    remarks = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task_progress'

    def __str__(self):
        return self.task.title