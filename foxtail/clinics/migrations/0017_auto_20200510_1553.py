# Generated by Django 3.0.5 on 2020-05-10 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0016_auto_20200510_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='end_time',
            field=models.CharField(choices=[('07:00', '7:00 AM'), ('08:00', '8:00 AM'), ('08:30', '8:30 AM'), ('09:00', '9:00 AM'), ('09:30', '9:30 AM'), ('10:00', '10:00 AM'), ('10:30', '10:30 AM'), ('11:00', '11:00 AM'), ('11:30', '11:30 AM'), ('12:00', '12:00 PM'), ('12:30', '12:30 PM'), ('13:00', '1:00 PM'), ('13:30', '1:30 PM'), ('14:00', '2:00 PM'), ('14:30', '2:30 PM'), ('15:00', '3:00 PM'), ('15:30', '3:30 PM'), ('16:00', '4:00 PM'), ('16:30', '4:30 PM'), ('17:00', '5:00 PM'), ('17:30', '5:30 PM'), ('18:00', '6:00 PM'), ('18:30', '6:30 PM'), ('19:00', '7:00 PM'), ('19:30', '7:30 PM'), ('20:00', '8:00 PM'), ('20:30', '8:30 PM')], max_length=255, verbose_name='End time'),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='start_time',
            field=models.CharField(choices=[('07:00', '7:00 AM'), ('08:00', '8:00 AM'), ('08:30', '8:30 AM'), ('09:00', '9:00 AM'), ('09:30', '9:30 AM'), ('10:00', '10:00 AM'), ('10:30', '10:30 AM'), ('11:00', '11:00 AM'), ('11:30', '11:30 AM'), ('12:00', '12:00 PM'), ('12:30', '12:30 PM'), ('13:00', '1:00 PM'), ('13:30', '1:30 PM'), ('14:00', '2:00 PM'), ('14:30', '2:30 PM'), ('15:00', '3:00 PM'), ('15:30', '3:30 PM'), ('16:00', '4:00 PM'), ('16:30', '4:30 PM'), ('17:00', '5:00 PM'), ('17:30', '5:30 PM'), ('18:00', '6:00 PM'), ('18:30', '6:30 PM'), ('19:00', '7:00 PM'), ('19:30', '7:30 PM'), ('20:00', '8:00 PM'), ('20:30', '8:30 PM')], max_length=255, verbose_name='Start time'),
        ),
    ]
