# Generated by Django 4.2.8 on 2024-06-06 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0044_alter_statustrackermaster_unique_together_and_more'),
        ('Sampling_db', '0040_delete_patternrequestmt'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatternRequestMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_no', models.CharField(max_length=30)),
                ('request_date', models.DateField(blank=True, null=True)),
                ('request_type', models.CharField(choices=[('F', 'Fresh'), ('C', 'Correction'), ('c', 'Consumption')], max_length=10)),
                ('buyer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('style_name', models.CharField(blank=True, max_length=100, null=True)),
                ('color_name', models.CharField(blank=True, max_length=100, null=True)),
                ('target_date', models.DateTimeField()),
                ('pattern_master', models.CharField(blank=True, max_length=100, null=True)),
                ('requirements', models.CharField(blank=True, max_length=100, null=True)),
                ('no_of_pattern_develop', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('merchant', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='pattern_request_merchant_name', to='IntelliSync_db.firstlevelmaster')),
                ('merchant_head', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='pattern_request_merchant_head', to='IntelliSync_db.commonmaster')),
                ('pattern_stage', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='pattern_request_pattern_stage', to='IntelliSync_db.commonmaster')),
                ('pattern_type', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='pattern_request_pattern_type', to='IntelliSync_db.firstlevelmaster')),
            ],
            options={
                'db_table': 'pattern_request_mt',
            },
        ),
    ]