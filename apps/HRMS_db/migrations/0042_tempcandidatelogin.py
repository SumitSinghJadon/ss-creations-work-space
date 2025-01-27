# Generated by Django 4.2.8 on 2024-06-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRMS_db', '0041_ticket_response_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempCandidateLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_no', models.CharField(editable=False, max_length=50, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'temp_candidate_login',
            },
        ),
    ]
