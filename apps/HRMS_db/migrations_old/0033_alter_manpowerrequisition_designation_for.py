# Generated by Django 4.2.8 on 2024-04-10 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll_db', '0005_leavebalance'),
        ('HRMS_db', '0032_alter_manpowerrequisition_designation_for_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manpowerrequisition',
            name='designation_for',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manpower_requisition_designation_for', to='Payroll_db.designationmaster'),
        ),
    ]