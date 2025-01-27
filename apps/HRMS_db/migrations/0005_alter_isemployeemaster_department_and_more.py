# Generated by Django 4.2.8 on 2024-02-23 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll_db', '0003_holidaymaster'),
        ('HRMS_db', '0004_alter_isemployeemaster_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isemployeemaster',
            name='department',
            field=models.ForeignKey(db_column='department', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='Payroll_db.departmentmaster'),
        ),
        migrations.AlterField(
            model_name='isemployeemaster',
            name='designation',
            field=models.ForeignKey(db_column='designation', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='Payroll_db.designationmaster'),
        ),
    ]
