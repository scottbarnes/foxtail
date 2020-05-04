""" foxtail/clinics/admin.py """
from django.contrib import admin

from .models import Clinic


# @admin.register(Clinic)
admin.site.register(Clinic)


