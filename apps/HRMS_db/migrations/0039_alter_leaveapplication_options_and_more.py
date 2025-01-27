# Generated by Django 4.2.8 on 2024-06-20 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0038_alter_leaveapplication_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaveapplication',
            options={'managed': False},
        ),
        migrations.AddField(
            model_name='manpowerrequisition',
            name='no_of_positions',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='manpowerrequisition',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('AHOD', 'Approved by HOD'), ('RHOD', 'Rejected by HOD'), ('AM', 'Approved by Management'), ('RM', 'Rejected by Management')], default='P', max_length=10),
        ),
    ]
