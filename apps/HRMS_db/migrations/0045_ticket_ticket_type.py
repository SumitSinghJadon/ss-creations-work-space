# Generated by Django 4.2.8 on 2024-07-05 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0044_tempcandidatelogin_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(blank=True, choices=[('S', 'Support'), ('R', 'Requirement')], max_length=10, null=True),
        ),
    ]
