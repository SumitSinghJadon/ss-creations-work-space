# Generated by Django 4.2.8 on 2024-07-02 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Payroll_db', '0005_leavebalance'),
        ('HRMS_db', '0043_delete_tempcandidatelogin_delete_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempCandidateLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_no', models.CharField(editable=False, max_length=50, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'temp_candidate_login',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('department', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_department', to='Payroll_db.departmentmaster')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
    ]
