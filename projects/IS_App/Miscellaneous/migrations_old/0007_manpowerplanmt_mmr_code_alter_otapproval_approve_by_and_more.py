# Generated by Django 4.2.8 on 2024-01-12 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Miscellaneous', '0006_otapproval'),
    ]

    operations = [
        migrations.AddField(
            model_name='manpowerplanmt',
            name='mmr_code',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otapproval',
            name='approve_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='otapproval',
            name='approve_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]