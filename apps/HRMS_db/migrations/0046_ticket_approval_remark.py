# Generated by Django 4.2.8 on 2024-07-05 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0045_ticket_ticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='approval_remark',
            field=models.TextField(blank=True, null=True),
        ),
    ]