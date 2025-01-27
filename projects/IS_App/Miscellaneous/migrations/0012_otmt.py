# Generated by Django 4.2.8 on 2024-01-16 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Miscellaneous', '0011_otapproval_approve_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTMT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_code', models.CharField(max_length=100)),
                ('dep_code', models.CharField(max_length=100)),
                ('ot_month', models.IntegerField()),
                ('ot_daily', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ot_mt',
            },
        ),
    ]
