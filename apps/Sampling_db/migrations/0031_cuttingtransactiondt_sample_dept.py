# Generated by Django 4.2.8 on 2024-04-14 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0030_otherentrymt_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuttingtransactiondt',
            name='sample_dept',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
