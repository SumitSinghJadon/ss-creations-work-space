# Generated by Django 4.2.8 on 2024-04-19 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0019_rename_mapping_id_statustrackermaster_application_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StatusTrackerMaster',
        ),
    ]
