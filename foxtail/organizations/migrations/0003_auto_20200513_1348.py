# Generated by Django 3.0.5 on 2020-05-13 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organization_abbreviation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.EmailField(max_length=40, verbose_name='Email'),
        ),
    ]
