# Generated by Django 4.2.8 on 2024-04-09 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntelliSync_db', '0030_alter_commonmastertype_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoIncrement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('next_no', models.PositiveBigIntegerField(default=321)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'auto_increment',
            },
        ),
    ]
