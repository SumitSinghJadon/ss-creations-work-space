# Generated by Django 4.2.8 on 2024-05-19 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QMS_db', '0009_alter_imagemaster_image1_alter_imagemaster_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderprocess',
            name='orderMT_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QMS_db.ordermt'),
        ),
        migrations.AlterField(
            model_name='orderprocess',
            name='sequence',
            field=models.IntegerField(),
        ),
    ]
