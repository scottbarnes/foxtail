""" foxtail/organizations/admin.py """
from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """ Admin panel options for the Organization model. """
    model = Organization
