# Generated by Django 4.2.8 on 2024-06-26 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QMS_db', '0014_qmsplaning'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'process_master',
            },
        ),
        migrations.DeleteModel(
            name='OperationMaster',
        ),
        migrations.RenameField(
            model_name='defectmaster',
            old_name='status',
            new_name='remarks',
        ),
        migrations.RemoveField(
            model_name='defectmaster',
            name='category',
        ),
        migrations.AddField(
            model_name='defectmaster',
            name='critical',
            field=models.CharField(blank=True, choices=[('MINOR', 'MINOR'), ('MAJOR', 'MAJOR')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='defectmaster',
            name='hindi_name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='defectmaster',
            name='is_reject',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='defectmaster',
            name='process',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='QMS_db.processmaster'),
        ),
    ]