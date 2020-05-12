# Generated by Django 3.0.5 on 2020-05-09 23:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinics', '0013_remove_clinic_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clinics_created', to=settings.AUTH_USER_MODEL),
        ),
    ]