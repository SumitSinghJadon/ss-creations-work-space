# Generated by Django 4.2.8 on 2024-04-03 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0030_alter_commonmastertype_code'),
        ('App_db', '0005_alter_tnatemplatemt_template_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tnatemplatedt',
            name='Base_activity',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='tna_base_activity', to='IntelliSync_db.firstlevelmaster'),
        ),
    ]