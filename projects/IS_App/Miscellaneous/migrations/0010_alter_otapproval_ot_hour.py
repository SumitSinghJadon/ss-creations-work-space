# Generated by Django 4.2.8 on 2024-01-12 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Miscellaneous', '0009_alter_otapproval_ot_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otapproval',
            name='ot_hour',
            field=models.IntegerField(),
        ),
    ]
