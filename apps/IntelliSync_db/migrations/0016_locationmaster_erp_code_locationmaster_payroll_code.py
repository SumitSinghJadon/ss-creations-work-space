# Generated by Django 4.2.8 on 2024-02-05 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0015_alter_firstlevelmaster_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationmaster',
            name='erp_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='locationmaster',
            name='payroll_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
