# Generated by Django 4.2.8 on 2024-07-15 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QMS_db', '0037_alter_rtqmmt_unique_together_rtqmmt_planing_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SewingLineInputDt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_qty', models.IntegerField(default=0)),
                ('entry_date', models.CharField(max_length=255)),
                ('entry_time', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sewing_line_input_dt',
            },
        ),
        migrations.CreateModel(
            name='SewingLineInputMt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_input_qty', models.IntegerField(default=0)),
                ('size', models.CharField(max_length=40)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('planing', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='QMS_db.qmsplaning')),
            ],
            options={
                'db_table': 'sewing_line_input_mt',
            },
        ),
        migrations.RemoveField(
            model_name='swinglineinputmt',
            name='planing',
        ),
        migrations.DeleteModel(
            name='SwingLineInputDt',
        ),
        migrations.DeleteModel(
            name='SwingLineInputMt',
        ),
        migrations.AddField(
            model_name='sewinglineinputdt',
            name='mt_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='QMS_db.sewinglineinputmt'),
        ),
    ]