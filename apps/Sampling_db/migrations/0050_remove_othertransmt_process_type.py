# Generated by Django 4.2.8 on 2024-06-14 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0049_patternrequestmt_pattern_cmd_date_and_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='othertransmt',
            name='process_type',
        ),
    ]
