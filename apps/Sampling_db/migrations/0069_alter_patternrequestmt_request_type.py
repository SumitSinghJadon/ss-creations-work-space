# Generated by Django 4.2.8 on 2024-07-16 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0068_alter_patternrequestmt_request_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patternrequestmt',
            name='request_type',
            field=models.CharField(choices=[('F', 'Fresh'), ('C', 'Correction'), ('S', 'Consumption')], max_length=10),
        ),
    ]
