# Generated by Django 4.2.8 on 2024-02-11 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('IntelliSync_db', '0019_alter_menumaster_parent_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CuttingTransactionDt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_no', models.TextField(blank=True, max_length=100, null=True)),
                ('cutting_type', models.TextField(blank=True, max_length=100, null=True)),
                ('cut_qty', models.TextField(blank=True, max_length=100, null=True)),
                ('size_breakup', models.TextField(blank=True, max_length=100, null=True)),
                ('cutter_name', models.TextField(blank=True, max_length=100, null=True)),
                ('assign_date', models.TextField(blank=True, max_length=100, null=True)),
                ('handover_to_supervisor', models.TextField(blank=True, max_length=100, null=True)),
                ('remarks', models.TextField(blank=True, max_length=100, null=True)),
                ('sample_status', models.TextField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'cutting_transaction_details',
            },
        ),
        migrations.CreateModel(
            name='PatternRequestMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_no', models.CharField(max_length=100)),
                ('request_date', models.DateField(blank=True, null=True)),
                ('request_type', models.TextField(blank=True, max_length=255, null=True)),
                ('pattern_stage', models.TextField(blank=True, max_length=255, null=True)),
                ('pattern_type', models.TextField(blank=True, max_length=255, null=True)),
                ('merchant', models.TextField(blank=True, max_length=255, null=True)),
                ('buyer_name', models.TextField(blank=True, max_length=255, null=True)),
                ('style_name', models.TextField(blank=True, max_length=255, null=True)),
                ('color_name', models.TextField(blank=True, max_length=255, null=True)),
                ('pattern_master', models.TextField(blank=True, max_length=255, null=True)),
                ('expected_del_date', models.DateField(blank=True, null=True)),
                ('expected_del_time', models.TimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'pattern_request_mt',
            },
        ),
        migrations.CreateModel(
            name='SampleBookingMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='sample booking/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='sample booking/')),
                ('booking_no', models.CharField(max_length=30)),
                ('booking_type', models.CharField(max_length=10)),
                ('buyer_code', models.CharField(blank=True, max_length=30, null=True)),
                ('buyer_name', models.CharField(blank=True, max_length=30, null=True)),
                ('style_no', models.CharField(blank=True, max_length=30, null=True)),
                ('booking_date', models.DateTimeField()),
                ('target_date', models.DateTimeField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('merchant_head', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_merchant_head', to='IntelliSync_db.commonmaster')),
                ('merchant_name', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_merchant_name', to='IntelliSync_db.firstlevelmaster')),
                ('product_type', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_product_type', to='IntelliSync_db.commonmaster')),
                ('sample_group_type', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_sample_type', to='IntelliSync_db.commonmaster')),
                ('sample_type', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_sample_type', to='IntelliSync_db.firstlevelmaster')),
                ('season', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_season', to='IntelliSync_db.commonmaster')),
                ('season_year', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_year', to='IntelliSync_db.firstlevelmaster')),
            ],
            options={
                'db_table': 'sample_booking_mt',
            },
        ),
        migrations.CreateModel(
            name='SampleSizeQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_no', models.CharField(max_length=30)),
                ('quantity', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sampling_db.samplebookingmt')),
                ('color', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_color', to='IntelliSync_db.commonmaster')),
                ('size', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='sbm_size', to='IntelliSync_db.commonmaster')),
            ],
            options={
                'db_table': 'sample_size_quantity',
            },
        ),
        migrations.CreateModel(
            name='SampleArticleDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_no', models.CharField(max_length=30)),
                ('given_by_merchant', models.CharField(max_length=30)),
                ('article_name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True, null=True)),
                ('expected_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sampling_db.samplebookingmt')),
            ],
            options={
                'db_table': 'sample_article_details',
            },
        ),
        migrations.CreateModel(
            name='CuttingTransactionMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_no', models.IntegerField(blank=True, null=True)),
                ('sample_booking_type', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='ctm_sample_booking_type', to='IntelliSync_db.commonmaster')),
            ],
            options={
                'db_table': 'sample_transaction_mt',
            },
        ),
        migrations.CreateModel(
            name='CuttingEntryMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_booking_type', models.DateTimeField()),
                ('sample_type', models.TextField(blank=True, max_length=100, null=True)),
                ('merchant_name', models.DateTimeField()),
                ('style_no', models.TextField(blank=True, max_length=100, null=True)),
                ('season', models.TextField(blank=True, max_length=100, null=True)),
                ('year', models.TextField(blank=True, max_length=100, null=True)),
                ('target_date', models.TextField(blank=True, max_length=100, null=True)),
                ('booked_date', models.TextField(blank=True, max_length=100, null=True)),
                ('qty', models.TextField(blank=True, max_length=100, null=True)),
                ('size', models.TextField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking_no', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='cem_booking_no', to='IntelliSync_db.commonmaster')),
                ('buyer', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='cem_buyer', to='IntelliSync_db.commonmaster')),
                ('merchant_group_name', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='cem_merchant_group_name', to='IntelliSync_db.commonmaster')),
            ],
            options={
                'db_table': 'cutting_entry_mt',
            },
        ),
        migrations.CreateModel(
            name='CheckerStatusMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliver_loss_time', models.DateTimeField()),
                ('remarks', models.TextField(blank=True, max_length=100, null=True)),
                ('returned_date', models.DateTimeField()),
                ('qa_remarks', models.TextField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('checker_status', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='csm_checker_status', to='IntelliSync_db.commonmaster')),
                ('delay_reason', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='csm_delay_reason', to='IntelliSync_db.commonmaster')),
                ('hold_reason', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='csm_hold_reason', to='IntelliSync_db.commonmaster')),
            ],
            options={
                'db_table': 'check_status_mt',
            },
        ),
    ]