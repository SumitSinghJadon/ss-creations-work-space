# Generated by Django 4.2.8 on 2024-06-03 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_db', '0016_buyerclaimmodel_amount_fc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyerclaimmodel',
            name='amount_fc',
        ),
    ]