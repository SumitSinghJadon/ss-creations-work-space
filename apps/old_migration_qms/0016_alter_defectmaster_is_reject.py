# Generated by Django 4.2.8 on 2024-06-26 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QMS_db', '0015_processmaster_delete_operationmaster_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defectmaster',
            name='is_reject',
            field=models.BooleanField(default=False),
        ),
    ]
