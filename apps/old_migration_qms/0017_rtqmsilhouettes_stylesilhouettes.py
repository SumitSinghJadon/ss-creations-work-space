# Generated by Django 4.2.8 on 2024-07-03 11:45

import QMS_db.models.rtqm_silhouettes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QMS_db', '0016_alter_defectmaster_is_reject'),
    ]

    operations = [
        migrations.CreateModel(
            name='RTQMSilhouettes',
            fields=[
                ('id', QMS_db.models.rtqm_silhouettes.RTQMDateID(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('buyer', models.CharField(max_length=100)),
                ('ourref', models.CharField(max_length=100)),
                ('style', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=20)),
                ('defect_operation', models.JSONField(default=list)),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'rtqm_silhouettes',
            },
        ),
        migrations.CreateModel(
            name='StyleSilhouettes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('front_image', models.ImageField(upload_to='assets/media/')),
                ('back_image', models.ImageField(upload_to='assets/media/')),
                ('buyer', models.CharField(max_length=50)),
                ('style_no', models.CharField(max_length=120)),
            ],
            options={
                'db_table': 'style_silhouettes',
                'unique_together': {('buyer', 'style_no')},
            },
        ),
    ]
