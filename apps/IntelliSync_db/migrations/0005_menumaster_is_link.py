# Generated by Django 4.2.8 on 2024-01-25 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0004_rename_local_url_modulemaster_dashboard_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumaster',
            name='is_link',
            field=models.BooleanField(default=False),
        ),
    ]
