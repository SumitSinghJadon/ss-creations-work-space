# Generated by Django 4.2.8 on 2024-03-04 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0016_leaveapplication_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveapplication',
            name='approved_by',
        ),
    ]
