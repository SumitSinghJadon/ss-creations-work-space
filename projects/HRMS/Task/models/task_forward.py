from django.db import models
from IntelliSync_db.models import User
from Task.models import TaskMasterMt


class TaskForwardMt(models.Model):
    task = models.ForeignKey(TaskMasterMt, on_delete=models.CASCADE)
    forward_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_forward_forward_to', db_constraint=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task_forward'

    def __str__(self):
        return self.task.title 