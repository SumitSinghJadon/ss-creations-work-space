# Generated by Django 4.2.8 on 2024-01-12 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Miscellaneous', '0007_manpowerplanmt_mmr_code_alter_otapproval_approve_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otapproval',
            name='dayno',
            field=models.DateField(),
        ),
    ]
