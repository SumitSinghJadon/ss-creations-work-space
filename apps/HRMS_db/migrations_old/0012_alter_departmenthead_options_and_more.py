# Generated by Django 4.2.8 on 2024-03-02 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Payroll_db', '0004_alter_timehourday_table'),
        ('IntelliSync_db', '0022_alter_commonmastertype_code'),
        ('HRMS_db', '0011_alter_leaveapplication_approved_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmenthead',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='isemployeemaster',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='leaveapplication',
            options={'managed': False},
        ),
        migrations.CreateModel(
            name='MeetingRoomMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(blank=True, max_length=100, null=True)),
                ('Remarks', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(blank=True, db_column='location', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='IntelliSync_db.locationmaster')),
            ],
            options={
                'db_table': 'meeting_room_master',
            },
        ),
        migrations.CreateModel(
            name='MeetingRoomBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_date', models.DateField(blank=True, null=True)),
                ('meeting_type', models.CharField(blank=True, choices=[('IN', 'Internal'), ('EX', 'External')], max_length=100, null=True)),
                ('start_time', models.CharField(blank=True, max_length=20, null=True)),
                ('end_time', models.CharField(blank=True, max_length=20, null=True)),
                ('purpose', models.CharField(blank=True, max_length=100, null=True)),
                ('booked_on', models.CharField(blank=True, max_length=100, null=True)),
                ('booked_by', models.CharField(blank=True, max_length=100, null=True)),
                ('guest_name', models.CharField(blank=True, max_length=100, null=True)),
                ('no_of_attendees', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('location', models.ForeignKey(blank=True, db_column='location', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='IntelliSync_db.locationmaster')),
                ('meeting_host', models.ForeignKey(blank=True, db_column='meeting_host', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Payroll_db.employeemaster')),
                ('room_name', models.ForeignKey(blank=True, db_column='room_name', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='HRMS_db.meetingroommaster')),
            ],
            options={
                'db_table': 'meeting_room_booking',
            },
        ),
    ]