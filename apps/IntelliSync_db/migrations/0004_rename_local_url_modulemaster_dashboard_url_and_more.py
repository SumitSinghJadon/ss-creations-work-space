# Generated by Django 4.2.8 on 2024-01-24 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0003_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modulemaster',
            old_name='local_url',
            new_name='dashboard_url',
        ),
        migrations.RemoveField(
            model_name='modulemaster',
            name='public_url',
        ),
        migrations.AddField(
            model_name='menumaster',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]