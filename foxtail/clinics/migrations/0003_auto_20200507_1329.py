# Generated by Django 3.0.5 on 2020-05-07 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0002_remove_clinic_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='end_time',
            field=models.CharField(choices=[('07:00:00', '7:00 AM'), ('07:30:00', '7:30 AM'), ('08:00:00', '8:00 AM'), ('08:30:00', '8:30 AM'), ('09:00:00', '9:00 AM'), ('09:30:00', '9:30 AM'), ('10:00:00', '10:00 AM'), ('10:30:00', '10:30 AM'), ('11:00:00', '11:00 AM'), ('11:30:00', '11:30 AM'), ('12:00:00', 'Noon'), ('12:30:00', '12:30 PM'), ('13:00:00', '1:00 PM'), ('13:30:00', '1:30 PM'), ('14:00:00', '2:00 PM'), ('14:30:00', '2:30 PM'), ('15:00:00', '3:00 PM'), ('15:30:00', '3:30 PM'), ('16:00:00', '4:00 PM'), ('16:30:00', '4:30 PM'), ('17:00:00', '5:00 PM'), ('17:30:00', '5:30 PM'), ('18:00:00', '6:00 PM'), ('18:30:00', '6:30 PM'), ('19:00:00', '7:00 PM'), ('19:30:00', '7:30 PM'), ('20:00:00', '8:00 PM'), ('20:30:00', '8:30 PM'), ('21:30:00', '9:00 PM'), ('21:00:00', '9:30 PM')], max_length=255, verbose_name='End time'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='start_time',
            field=models.CharField(choices=[('07:00:00', '7:00 AM'), ('07:30:00', '7:30 AM'), ('08:00:00', '8:00 AM'), ('08:30:00', '8:30 AM'), ('09:00:00', '9:00 AM'), ('09:30:00', '9:30 AM'), ('10:00:00', '10:00 AM'), ('10:30:00', '10:30 AM'), ('11:00:00', '11:00 AM'), ('11:30:00', '11:30 AM'), ('12:00:00', 'Noon'), ('12:30:00', '12:30 PM'), ('13:00:00', '1:00 PM'), ('13:30:00', '1:30 PM'), ('14:00:00', '2:00 PM'), ('14:30:00', '2:30 PM'), ('15:00:00', '3:00 PM'), ('15:30:00', '3:30 PM'), ('16:00:00', '4:00 PM'), ('16:30:00', '4:30 PM'), ('17:00:00', '5:00 PM'), ('17:30:00', '5:30 PM'), ('18:00:00', '6:00 PM'), ('18:30:00', '6:30 PM'), ('19:00:00', '7:00 PM'), ('19:30:00', '7:30 PM'), ('20:00:00', '8:00 PM'), ('20:30:00', '8:30 PM'), ('21:30:00', '9:00 PM'), ('21:00:00', '9:30 PM')], max_length=255, verbose_name='Start time'),
        ),
    ]
