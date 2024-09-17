from django.db import models
from Payroll_db.models import DepartmentMaster
from IS_Nexus.database.is_hrms import getEmployeeDetails
from IntelliSync_db.models import LocationMaster
from HRMS_db.models import ManPowerRequisition

class JobApplicationForm(models.Model):

    sex_list = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('A','Other')
    )

    maritial_status_list={
        ('U','Unmarried'),
        ('M','Married'),
        ('D','Divorced')
    }

    application_no = models.CharField(max_length=50, unique=True, editable=False)
    dob = models.DateField()
    contact_no=models.CharField(max_length=10,unique=True,editable=False)
    username = models.CharField(max_length=50)
    post_applied_for = models.ForeignKey(ManPowerRequisition, on_delete=models.DO_NOTHING,null=True,blank=True)
    father_or_husband_name = models.CharField(max_length=100,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    sex = models.CharField(max_length=10,null=True,blank=True,choices=sex_list)
    age = models.IntegerField(null=True,blank=True)
    maritial_status = models.CharField(max_length=10,null=True,blank=True,choices=maritial_status_list)
    spouse = models.CharField(max_length=100,null=True,blank=True)
    occupation = models.CharField(max_length=100,null=True,blank=True)
    no_of_dependents = models.IntegerField(null=True,blank=True)
    nationality = models.CharField(max_length=100,null=True,blank=True)
    religion = models.CharField(max_length=100,null=True,blank=True)
    caste = models.CharField(max_length=100,null=True,blank=True)
    region = models.CharField(max_length=100,null=True,blank=True)
    present_address = models.CharField(max_length=100,null=True,blank=True)
    present_district = models.CharField(max_length=100,null=True,blank=True) 
    present_city = models.CharField(max_length=100,null=True,blank=True)
    present_state = models.CharField(max_length=100,null=True,blank=True)
    present_country = models.CharField(max_length=100,null=True,blank=True)
    present_pin = models.CharField(max_length=100,null=True,blank=True)
    present_phone_own = models.CharField(max_length=100,null=True,blank=True)
    present_phone_residence = models.CharField(max_length=100,null=True,blank=True)
    permanent_address = models.CharField(max_length=100,null=True,blank=True)
    permanent_district = models.CharField(max_length=100,null=True,blank=True) 
    permanent_city = models.CharField(max_length=100,null=True,blank=True)
    permanent_state = models.CharField(max_length=100,null=True,blank=True)
    permanent_country = models.CharField(max_length=100,null=True,blank=True)
    permanent_pin = models.CharField(max_length=100,null=True,blank=True)
    permanent_phone_own = models.CharField(max_length=100,null=True,blank=True)
    permanent_phone_residence = models.CharField(max_length=100,null=True,blank=True)
    interviewed_by_us = models.BooleanField(default=False)
    date_of_interview = models.DateField(null=True,blank=True)
    interviewed_by = models.CharField(max_length=100,null=True,blank=True)
    major_achievement= models.TextField(null=True,blank=True)
    career_goals = models.TextField(null=True,blank=True)
    related_company_person=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_filled=models.IntegerField(default=0)
    passport_photo = models.FileField(upload_to='job_application/', blank=True, null=True)
    resume = models.FileField(upload_to='job_application/', blank=True, null=True)
    class Meta:
        db_table = 'job_application'
        app_label = 'HRMS_db'
        unique_together  = ('application_no','contact_no','dob')


class Language_known(models.Model):
    job_application = models.ForeignKey(JobApplicationForm,db_constraint=False,on_delete=models.DO_NOTHING,related_name='job_application_language_known')
    language = models.CharField(max_length=100,null=True,blank=True)
    speak = models.BooleanField(default=False) 
    read = models.BooleanField(default=False) 
    write = models.BooleanField(default=False) 

    class Meta:
        db_table='language_known'
        app_label='HRMS_db'

class Qualification(models.Model):
    job_application = models.ForeignKey(JobApplicationForm,db_constraint=False,on_delete=models.DO_NOTHING,related_name='job_application_qualification')
    type = models.CharField(max_length=100,null=True,blank=True)
    degree = models.CharField(max_length=100,null=True,blank=True)
    university = models.CharField(max_length=100,null=True,blank=True)
    year = models.CharField(max_length=100,null=True,blank=True)
    main_subject = models.CharField(max_length=100,null=True,blank=True)
    division = models.CharField(max_length=100,null=True,blank=True)
    special_remarks = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table='job_application_qualification'
        app_label='HRMS_db'

class EmploymentRecord(models.Model):
    job_application = models.ForeignKey(JobApplicationForm,db_constraint=False,on_delete=models.DO_NOTHING,related_name='job_application_employment_record')
    period = models.CharField(max_length=100,null=True,blank=True)
    employer = models.CharField(max_length=100,null=True,blank=True)
    designation = models.CharField(max_length=100,null=True,blank=True)
    address_phn_no = models.CharField(max_length=100,null=True,blank=True)
    last_salary = models.CharField(max_length=100,null=True,blank=True)
    reason_for_leaving = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table='job_application_employment_record'
        app_label='HRMS_db'

class FamilyDetails(models.Model):
    job_application = models.ForeignKey(JobApplicationForm,db_constraint=False,on_delete=models.DO_NOTHING,related_name='job_application_family_details')
    family_member = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    age_or_year_of_birth = models.CharField(max_length=100,null=True,blank=True)
    relation = models.CharField(max_length=100,null=True,blank=True)
    residing = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table='job_application_family_details'
        app_label='HRMS_db'

class ReferenceDetails(models.Model):
    job_application = models.ForeignKey(JobApplicationForm,db_constraint=False,on_delete=models.DO_NOTHING,related_name='job_application_reference')
    name = models.CharField(max_length=100,null=True,blank=True)
    occupation = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    phone_no = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table='job_application_reference_details'
        app_label='HRMS_db'

class RelatedCompanyPerson(models.Model):
    job_application = models.ForeignKey(JobApplicationForm,db_constraint=False,on_delete=models.DO_NOTHING,related_name='job_application_related')
    name = models.CharField(max_length=100,null=True,blank=True)
    designation = models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=255,null=True,blank=True)
    relation = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table='job_application_related_person'
        app_label='HRMS_db'
