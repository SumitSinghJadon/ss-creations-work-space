# Generated by Django 4.2.8 on 2024-02-29 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0017_alter_samplebookingmt_booking_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplebookingmt',
            name='cancelled_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
