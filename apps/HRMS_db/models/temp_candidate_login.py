from django.db import models, transaction, IntegrityError
import datetime

class TempCandidateLogin(models.Model):
    application_no = models.CharField(max_length=50, unique=True, editable=False)
    username = models.CharField(max_length=50)
    dob = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'temp_candidate_login'
        app_label = 'HRMS_db'
        unique_together  = ('username','dob')

    def save(self, *args, **kwargs):
        if not self.application_no:
            self.application_no = self.generate_unique_application_no()
        super().save(*args, **kwargs)

