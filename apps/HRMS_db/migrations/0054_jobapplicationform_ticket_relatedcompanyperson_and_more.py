# Generated by Django 4.2.8 on 2024-07-13 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Payroll_db', '0005_leavebalance'),
        ('IntelliSync_db', '0044_alter_statustrackermaster_unique_together_and_more'),
        ('HRMS_db', '0053_delete_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplicationForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_no', models.CharField(editable=False, max_length=50, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('father_or_husband_name', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('sex', models.CharField(blank=True, max_length=10, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('maritial_status', models.CharField(blank=True, max_length=10, null=True)),
                ('spouse', models.CharField(blank=True, max_length=100, null=True)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('no_of_dependents', models.IntegerField(blank=True, null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('caste', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('present_address', models.CharField(blank=True, max_length=100, null=True)),
                ('present_district', models.CharField(blank=True, max_length=100, null=True)),
                ('present_city', models.CharField(blank=True, max_length=100, null=True)),
                ('present_state', models.CharField(blank=True, max_length=100, null=True)),
                ('present_country', models.CharField(blank=True, max_length=100, null=True)),
                ('present_pin', models.CharField(blank=True, max_length=100, null=True)),
                ('present_phone_own', models.CharField(blank=True, max_length=100, null=True)),
                ('present_phone_residence', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_district', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_city', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_state', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_country', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_pin', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_phone_own', models.CharField(blank=True, max_length=100, null=True)),
                ('permanent_phone_residence', models.CharField(blank=True, max_length=100, null=True)),
                ('interviewed_by_us', models.BooleanField(default=False)),
                ('date_of_interview', models.DateField(blank=True, null=True)),
                ('interviewed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('major_achievement', models.TextField(blank=True, null=True)),
                ('career_goals', models.TextField(blank=True, null=True)),
                ('related_company_person', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_filled', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'job_application',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_type', models.CharField(choices=[('S', 'Support'), ('R', 'Requirement')], max_length=10)),
                ('support_department_name', models.CharField(blank=True, max_length=100, null=True)),
                ('response_date', models.DateTimeField(blank=True, null=True)),
                ('closer_date', models.DateTimeField()),
                ('selection_action_about_task', models.CharField(blank=True, max_length=100, null=True)),
                ('helpdesk_image', models.ImageField(blank=True, null=True, upload_to='helpdesk_images/')),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('remarks', models.CharField(blank=True, max_length=250, null=True)),
                ('reason', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('IP', 'In Progress'), ('NMA', 'Need Management Approval'), ('A', 'Approved'), ('D', 'Done'), ('C', 'Completed')], default='P', max_length=10)),
                ('expected_date', models.DateTimeField(blank=True, null=True)),
                ('problems', models.TextField(blank=True, null=True)),
                ('reason_not_done', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approval_remark', models.TextField(blank=True, null=True)),
                ('management_approval', models.BooleanField(default=False)),
                ('department_title', models.CharField(blank=True, max_length=255, null=True)),
                ('management_description', models.TextField(blank=True, null=True)),
                ('management_status', models.CharField(choices=[('P', 'Pending'), ('IP', 'In Progress'), ('NMA', 'Need Management Approval'), ('A', 'Approved'), ('D', 'Done'), ('C', 'Completed')], default='P', max_length=10)),
                ('department_description', models.TextField(blank=True, null=True)),
                ('department', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_department', to='Payroll_db.departmentmaster')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='RelatedCompanyPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=255, null=True)),
                ('relation', models.CharField(blank=True, max_length=100, null=True)),
                ('job_application', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_application_related', to='HRMS_db.jobapplicationform')),
            ],
            options={
                'db_table': 'job_application_related_person',
            },
        ),
        migrations.CreateModel(
            name='ReferenceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=100, null=True)),
                ('job_application', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_application_reference', to='HRMS_db.jobapplicationform')),
            ],
            options={
                'db_table': 'job_application_reference_details',
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('degree', models.CharField(blank=True, max_length=100, null=True)),
                ('university', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=100, null=True)),
                ('main_subject', models.CharField(blank=True, max_length=100, null=True)),
                ('division', models.CharField(blank=True, max_length=100, null=True)),
                ('special_remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('job_application', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_application_qualification', to='HRMS_db.jobapplicationform')),
            ],
            options={
                'db_table': 'job_application_qualification',
            },
        ),
        migrations.CreateModel(
            name='ManPowerRequisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(blank=True, choices=[('N', 'New'), ('R', 'Replacement'), ('A', 'Any')], max_length=20, null=True)),
                ('sub_department', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_salary', models.CharField(blank=True, max_length=100, null=True)),
                ('justification', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('AHOD', 'Approved by HOD'), ('RHOD', 'Rejected by HOD'), ('AM', 'Approved by Management'), ('RM', 'Rejected by Management')], default='P', max_length=10)),
                ('no_of_positions', models.CharField(blank=True, max_length=10, null=True)),
                ('salary_range', models.CharField(blank=True, max_length=100, null=True)),
                ('suggested_salary_range', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_year_range', models.CharField(blank=True, max_length=10, null=True)),
                ('age_range', models.CharField(blank=True, max_length=10, null=True)),
                ('special_skill_required', models.TextField(blank=True, null=True)),
                ('preferred_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('A', 'Any')], default='A', max_length=20)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('department_for', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_department_for', to='Payroll_db.departmentmaster')),
                ('designation_for', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_designation_for', to='Payroll_db.designationmaster')),
                ('job_location', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_job_location', to='IntelliSync_db.locationmaster')),
                ('replacement_employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_replacement_for', to=settings.AUTH_USER_MODEL)),
                ('report_to', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_report_to', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'manpower_requisition',
            },
        ),
        migrations.CreateModel(
            name='ManpowerQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manpower', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_qualification', to='HRMS_db.manpowerrequisition')),
                ('qualification', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='IntelliSync_db.commonmaster')),
            ],
            options={
                'db_table': 'manpower_requisition_degree',
            },
        ),
        migrations.CreateModel(
            name='ManpowerPreferredResidentLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manpower', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_preffered_resident_location', to='HRMS_db.manpowerrequisition')),
                ('preferred_resident_location', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='IntelliSync_db.secondlevelmaster')),
            ],
            options={
                'db_table': 'manpower_requisition_location',
            },
        ),
        migrations.CreateModel(
            name='Language_known',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('speak', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('write', models.BooleanField(default=False)),
                ('job_application', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_application_language_known', to='HRMS_db.jobapplicationform')),
            ],
            options={
                'db_table': 'language_known',
            },
        ),
        migrations.AddField(
            model_name='jobapplicationform',
            name='post_applied_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='HRMS_db.manpowerrequisition'),
        ),
        migrations.CreateModel(
            name='FamilyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_member', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('age_or_year_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('relation', models.CharField(blank=True, max_length=100, null=True)),
                ('residing', models.CharField(blank=True, max_length=100, null=True)),
                ('job_application', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_application_family_details', to='HRMS_db.jobapplicationform')),
            ],
            options={
                'db_table': 'job_application_family_details',
            },
        ),
        migrations.CreateModel(
            name='EmploymentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(blank=True, max_length=100, null=True)),
                ('employer', models.CharField(blank=True, max_length=100, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('address_phn_no', models.CharField(blank=True, max_length=100, null=True)),
                ('last_salary', models.CharField(blank=True, max_length=100, null=True)),
                ('reason_for_leaving', models.CharField(blank=True, max_length=100, null=True)),
                ('job_application', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='job_application_employment_record', to='HRMS_db.jobapplicationform')),
            ],
            options={
                'db_table': 'job_application_employment_record',
            },
        ),
        migrations.AlterUniqueTogether(
            name='jobapplicationform',
            unique_together={('username', 'dob')},
        ),
    ]
