# Generated by Django 4.2.8 on 2024-07-03 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_db', '0026_merge_20240622_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnergyCostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=50)),
                ('head', models.CharField(max_length=50)),
                ('sub_head', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('reading', models.FloatField(default=0.0, null=True)),
                ('cons_hr', models.FloatField(default=0.0, null=True)),
                ('consumption', models.FloatField(default=0.0, null=True)),
                ('fuel_consumed', models.FloatField(default=0.0, null=True)),
                ('running_unit', models.FloatField(default=0.0, null=True)),
                ('kwh_reading', models.FloatField(default=0.0, null=True)),
                ('multiplier', models.FloatField(default=0.0, null=True)),
                ('unit_consumed', models.FloatField(default=0.0, null=True)),
                ('unit_consumed_kvah', models.FloatField(default=0.0, null=True)),
                ('unit_consumed_kwh', models.FloatField(default=0.0, null=True)),
                ('kvah_reading', models.FloatField(default=0.0, null=True)),
                ('power_factor', models.FloatField(default=0.0, null=True)),
                ('rate', models.FloatField(default=0.0)),
                ('energy_value', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'energy_cost',
            },
        ),
        migrations.DeleteModel(
            name='TnaTemplateDt',
        ),
        migrations.DeleteModel(
            name='TnaTemplateMt',
        ),
    ]