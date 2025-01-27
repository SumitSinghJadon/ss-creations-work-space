# Generated by Django 4.2.8 on 2024-07-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QMS_db', '0025_alter_rtqmmt_total_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rtqmcounter',
            name='rectified',
            field=models.CharField(choices=[('RCT', 'RECTIFIED'), ('D', 'DEFECT'), ('R', 'REJECT')], max_length=10),
        ),
        migrations.AlterField(
            model_name='rtqmcounter',
            name='status',
            field=models.CharField(choices=[('RFT', 'PASS'), ('D', 'DEFECT'), ('R', 'REJECT')], max_length=10),
        ),
    ]
