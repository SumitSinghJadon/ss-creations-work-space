# Generated by Django 4.2.8 on 2024-03-04 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0018_leaveapplication_updated_by'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='leaveapplication',
            table='application',
        ),
    ]
