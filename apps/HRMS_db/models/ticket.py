from django.db import models
from IntelliSync_db.models import User
from Payroll_db.models import DepartmentMaster
from IntelliSync_db.models.location_master import LocationMaster
class Ticket(models.Model):
    status_list = (
    ('P', 'Pending'),
    ('IP','In Progress'),
    ('NMA','Need Management Approval'),
    ('A','Approved'),
    ('D','Done'),
    ('C','Completed')
    )
    ticket_type_list=(
        ('S','Support'),
        ('R','Requirement'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False,related_name='ticket_user')
    ticket_type=models.CharField(max_length=10, choices=ticket_type_list)
    support_department_name = models.CharField(max_length=100,null=True,blank=True)
    department = models.ForeignKey(DepartmentMaster,on_delete=models.CASCADE, related_name='ticket_department', db_constraint=False)
    response_date = models.DateTimeField(blank=True,null=True)
    closer_date = models.DateTimeField()
    selection_action_about_task=models.CharField(max_length=100,null=True,blank=True)
    helpdesk_image = models.ImageField(upload_to='helpdesk_images/', blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    reason=models.CharField(max_length=250,blank=True ,null=True)
    status = models.CharField(max_length=10, default='P', choices=status_list)
    expected_date=models.DateTimeField(null=True,blank=True)
    updated_by=models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False,related_name='ticket_updated_by',null=True,blank=True)
    problems = models.TextField(null=True,blank=True)
    reason_not_done = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approval_remark=models.TextField(null=True,blank=True)
    management_approval=models.BooleanField(default=False)
    department_title=models.CharField(max_length=255,null=True,blank=True)
    management_description= models.TextField(null=True,blank=True)
    management_status=models.CharField(max_length=10, default='P', choices=status_list)
    department_description= models.TextField(null=True,blank=True)


    
    def str(self):
        return f"Ticket {self.id} - {self.support_department_name}"
    class Meta:
        db_table = 'ticket'
        app_label = 'HRMS_db'