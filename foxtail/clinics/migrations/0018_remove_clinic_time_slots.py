# Generated by Django 3.0.5 on 2020-05-10 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0017_auto_20200510_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinic',
            name='time_slots',
        ),
    ]
