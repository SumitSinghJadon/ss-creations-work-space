# Generated by Django 4.2.8 on 2024-02-05 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0016_locationmaster_erp_code_locationmaster_payroll_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymaster',
            name='address',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companymaster',
            name='cin',
            field=models.CharField(default='test', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companymaster',
            name='gstin',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AddField(
            model_name='companymaster',
            name='pan',
            field=models.CharField(default='test', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locationmaster',
            name='gstin',
            field=models.CharField(default='test', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]