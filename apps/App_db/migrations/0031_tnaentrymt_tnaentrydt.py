# Generated by Django 4.2.8 on 2024-07-04 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_db', '0030_remove_tnaentrymt_tna_template_delete_tnaentrydt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TnaEntryMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tna_entry_no', models.CharField(max_length=30)),
                ('buyer_code', models.CharField(max_length=100)),
                ('buyer_name', models.CharField(max_length=255)),
                ('style', models.CharField(max_length=255)),
                ('ref_no', models.CharField(max_length=255)),
                ('delivery_date', models.DateField()),
                ('order_date', models.DateField()),
                ('pcd_date', models.DateField()),
                ('lead_time', models.IntegerField()),
                ('tna_entry_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tna_template', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='App_db.tnatemplatemt')),
            ],
            options={
                'db_table': 'tna_entry_mt',
            },
        ),
        migrations.CreateModel(
            name='TnaEntryDt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=255)),
                ('before_after', models.CharField(max_length=255)),
                ('base_activity', models.CharField(max_length=255)),
                ('days', models.IntegerField()),
                ('running_days', models.IntegerField()),
                ('plan_date_start', models.DateField()),
                ('plan_date_end', models.DateField()),
                ('plan_week_day', models.IntegerField()),
                ('res_person', models.CharField(max_length=255)),
                ('res_department', models.CharField(max_length=255)),
                ('actual_dates', models.DateField()),
                ('status', models.CharField(max_length=30)),
                ('remark', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tna_mt', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='App_db.tnaentrymt')),
            ],
            options={
                'db_table': 'tna_entry_dt',
            },
        ),
    ]