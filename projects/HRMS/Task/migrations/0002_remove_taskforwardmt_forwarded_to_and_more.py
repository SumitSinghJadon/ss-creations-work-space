# Generated by Django 4.2.8 on 2023-12-18 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Task', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskforwardmt',
            name='forwarded_to',
        ),
        migrations.AddField(
            model_name='taskforwardmt',
            name='forward_to',
            field=models.ForeignKey(db_constraint=False, default='1', on_delete=django.db.models.deletion.CASCADE, related_name='task_forward_forward_to', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
