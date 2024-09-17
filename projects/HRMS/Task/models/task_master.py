from django.db import models
from IntelliSync_db.models import User


class TaskMasterMt(models.Model):
    status_list = (
        ('assigned', 'Assigned'),
        ('pending', 'Pending'), 
        ('suggested', 'Suggested'),
        ('in-process', 'In-process'),
        ('completed', 'Completed'),
        ('rejected', 'rejected'),
        ('finished', 'Finished'),
    )

    frequency_list = (
        ('one_time', 'One Time'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half Yearly'),
        ('yearly', 'Yearly')
    )

    priority_list = (
         ('normal', 'Normal'),
	     ('high', 'High'),
	     ('medium', 'Medium'),
	     ('immediate', 'Immediate'),
    )

    user = models.ManyToManyField(User, db_constraint=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_master_owner', db_constraint=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    frequency = models.CharField(max_length=80, choices=frequency_list)
    priority =models.CharField(max_length=80, choices = priority_list)
    # remainder = models.DateTimeField()
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=80, choices=status_list)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_master_created_by', db_constraint=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task_master'

    def __str__(self):
        return self.title