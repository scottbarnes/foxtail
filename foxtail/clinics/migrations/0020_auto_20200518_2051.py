# Generated by Django 3.0.5 on 2020-05-18 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0019_clinicproxy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clinic',
            options={'verbose_name': 'Tabular clinic view', 'verbose_name_plural': 'Tabular clinic views'},
        ),
        migrations.AlterModelOptions(
            name='clinicproxy',
            options={'verbose_name': 'Stacked clinic view', 'verbose_name_plural': 'Stacked clinic views'},
        ),
    ]
