# Generated by Django 5.1.6 on 2025-02-13 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorschedule',
            name='doctor',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='DoctorSchedule',
        ),
    ]
