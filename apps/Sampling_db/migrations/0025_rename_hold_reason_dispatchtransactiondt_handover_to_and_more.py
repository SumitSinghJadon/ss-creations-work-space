# Generated by Django 4.2.8 on 2024-03-14 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0024_dispatchtransactiondt_dispatchentrymt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dispatchtransactiondt',
            old_name='hold_reason',
            new_name='handover_to',
        ),
        migrations.RemoveField(
            model_name='dispatchtransactiondt',
            name='qa_name',
        ),
        migrations.RemoveField(
            model_name='dispatchtransactiondt',
            name='qa_remarks',
        ),
        migrations.RemoveField(
            model_name='dispatchtransactiondt',
            name='qa_status',
        ),
        migrations.RemoveField(
            model_name='dispatchtransactiondt',
            name='return_date',
        ),
    ]
