# Generated by Django 4.2.8 on 2024-06-03 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_db', '0014_buyerclaimmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyerclaimmodel',
            name='currency',
            field=models.CharField(max_length=5),
        ),
    ]