# Generated by Django 4.2.8 on 2024-07-05 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0058_alter_raformmt_merchant_head_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raformmt',
            name='style_risk_category',
            field=models.CharField(blank=True, choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], max_length=20, null=True),
        ),
    ]
