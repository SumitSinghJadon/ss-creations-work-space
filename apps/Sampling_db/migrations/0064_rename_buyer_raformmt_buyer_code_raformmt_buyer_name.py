# Generated by Django 4.2.8 on 2024-07-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sampling_db', '0063_remove_raformdt_category_index_raformdt_mt_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raformmt',
            old_name='buyer',
            new_name='buyer_code',
        ),
        migrations.AddField(
            model_name='raformmt',
            name='buyer_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]