# Generated by Django 4.2.8 on 2024-06-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0054_alter_patternrequestmt_pattern_done_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patternrequestmt',
            name='pattern_master_remarks',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]