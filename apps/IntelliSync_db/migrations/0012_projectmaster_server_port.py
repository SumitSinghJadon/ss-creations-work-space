# Generated by Django 4.2.8 on 2024-02-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0011_companymaster_server_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmaster',
            name='server_port',
            field=models.IntegerField(default=8000),
        ),
    ]