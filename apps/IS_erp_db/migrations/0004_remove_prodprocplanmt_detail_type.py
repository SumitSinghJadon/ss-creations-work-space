# Generated by Django 4.2.8 on 2024-09-09 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IS_erp_db', '0003_alter_prodprocplanmt_u_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prodprocplanmt',
            name='detail_type',
        ),
    ]