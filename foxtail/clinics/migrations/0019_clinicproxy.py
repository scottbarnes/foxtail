# Generated by Django 3.0.5 on 2020-05-18 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0018_remove_clinic_time_slots'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('clinics.clinic',),
        ),
    ]
