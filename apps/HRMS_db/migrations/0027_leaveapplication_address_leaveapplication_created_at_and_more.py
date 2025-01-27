# Generated by Django 4.2.8 on 2024-04-30 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HRMS_db', '0026_alter_leaveapplication_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='from_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='reason',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='till_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='time',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='updated_by',
            field=models.ForeignKey(blank=True, db_column='updated_by', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='leave_application_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='user',
            field=models.ForeignKey(db_constraint=False, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='leave_application_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='applications/'),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterUniqueTogether(
            name='leaveapplication',
            unique_together={('user', 'dep', 'application_type', 'leave_type', 'from_date', 'till_date', 'time', 'working_day', 'day_part', 'day_count', 'reason', 'address', 'visit_location_type', 'mobile_number', 'status', 'attachment')},
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='address_on_leave',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='approval_remarks',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='emp_name',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='emp_paycode',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='leave_from',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='leave_till',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='mis_in_time',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='mis_out_time',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='purpose_of_visit',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='reason_for_leave',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='reporting_manager',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='visit_location',
        ),
    ]
