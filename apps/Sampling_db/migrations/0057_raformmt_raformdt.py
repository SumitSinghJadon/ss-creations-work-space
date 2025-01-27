# Generated by Django 4.2.8 on 2024-07-04 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0044_alter_statustrackermaster_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Sampling_db', '0056_patternrequestmt_buyer_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaFormMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ra_no', models.CharField(max_length=30)),
                ('ra_date', models.DateField(blank=True, null=True)),
                ('style_no', models.CharField(blank=True, max_length=200, null=True)),
                ('buyer', models.CharField(blank=True, max_length=200, null=True)),
                ('product_type', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_department', models.CharField(blank=True, max_length=200, null=True)),
                ('po_number', models.CharField(blank=True, max_length=200, null=True)),
                ('erp_order', models.CharField(blank=True, max_length=200, null=True)),
                ('order_qty', models.CharField(blank=True, max_length=200, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('style_risk_category', models.CharField(blank=True, max_length=200, null=True)),
                ('area_of_risk', models.TextField(blank=True, null=True)),
                ('picture_of_style', models.ImageField(blank=True, null=True, upload_to='ra_booking/')),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.CharField(blank=True, max_length=200, null=True)),
                ('shell', models.TextField(blank=True, null=True)),
                ('trim', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ra_status_mt_created_by', to=settings.AUTH_USER_MODEL)),
                ('merchant_head', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ra_merchant_head', to='IntelliSync_db.commonmaster')),
                ('merchant_name', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ra_merchant_name', to='IntelliSync_db.firstlevelmaster')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ra_status_mt_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ra_status_mt',
            },
        ),
        migrations.CreateModel(
            name='RaFormDt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=200, null=True)),
                ('category_index', models.FloatField(blank=True, null=True)),
                ('category_content', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ra_form_dt_category_content', to=settings.AUTH_USER_MODEL)),
                ('ra_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sampling_db.raformmt')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ra_form_dt',
            },
        ),
    ]
