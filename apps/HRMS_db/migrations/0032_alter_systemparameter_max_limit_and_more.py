# Generated by Django 4.2.8 on 2024-05-07 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0031_systemparameter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemparameter',
            name='max_limit',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='systemparameter',
            name='min_limit',
            field=models.CharField(max_length=10),
        ),
    ]