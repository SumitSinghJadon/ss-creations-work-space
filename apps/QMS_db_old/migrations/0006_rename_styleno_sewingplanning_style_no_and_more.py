# Generated by Django 4.2.8 on 2024-07-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QMS_db', '0005_rename_rtqm_counter_sewingendlinedefect_counter_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sewingplanning',
            old_name='styleno',
            new_name='style_no',
        ),
        migrations.AddField(
            model_name='sewingplanning',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
