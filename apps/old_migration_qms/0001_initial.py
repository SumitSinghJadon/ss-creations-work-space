# Generated by Django 4.2.8 on 2024-04-01 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='media/')),
                ('image2', models.ImageField(upload_to='media/')),
                ('buyer', models.CharField(max_length=50)),
                ('style', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='OrderMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_order_no', models.CharField(blank=True, max_length=20, null=True)),
                ('ourref_no', models.CharField(blank=True, max_length=100, null=True)),
                ('style_no', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('style_name', models.CharField(blank=True, max_length=100, null=True)),
                ('Style_category', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'order_mt',
                'unique_together': {('ourref_no', 'style_no', 'color')},
            },
        ),
        migrations.CreateModel(
            name='OrderProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(max_length=20)),
                ('process', models.CharField(max_length=50)),
                ('orderMT_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QMS_db.ordermt')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('order_dt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QMS_db.ordermt')),
            ],
            options={
                'db_table': 'order_dt',
            },
        ),
    ]