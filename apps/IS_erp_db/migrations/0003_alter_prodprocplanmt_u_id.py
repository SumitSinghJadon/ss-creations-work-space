# Generated by Django 4.2.8 on 2024-09-07 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0046_statustrackermaster'),
        ('IS_erp_db', '0002_remove_prodprocplanmt_plan_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodprocplanmt',
            name='u_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='IntelliSync_db.locationmaster'),
        ),
    ]
