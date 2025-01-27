# Generated by Django 4.2.8 on 2024-04-08 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HRMS_db', '0028_manpowerrequisition'),
    ]

    operations = [
        migrations.AddField(
            model_name='manpowerrequisition',
            name='department_for',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='manpowerrequisition',
            name='designation_for',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='manpowerrequisition',
            name='management_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='manpowerrequisition',
            name='prop_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='manpowerrequisition',
            name='replacement_employee',
            field=models.ForeignKey(db_constraint=False, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_replacement_employee', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manpowerrequisition',
            name='why_replacement',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='manpowerrequisition',
            name='qualification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
