# Generated by Django 4.2.8 on 2024-07-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_db', '0038_overheadmt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tnaentrydt',
            old_name='before_after',
            new_name='days_action',
        ),
        migrations.RenameField(
            model_name='tnaentrydt',
            old_name='days',
            new_name='days_before_after',
        ),
        migrations.RemoveField(
            model_name='tnaentrydt',
            name='actual_dates',
        ),
        migrations.RemoveField(
            model_name='tnaentrydt',
            name='status',
        ),
        migrations.AddField(
            model_name='tnaentrydt',
            name='days_req',
            field=models.IntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='overheadmt',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tnaentrydt',
            name='base_activity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tnaentrydt',
            name='plan_week_day',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tnaentrydt',
            name='remark',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
