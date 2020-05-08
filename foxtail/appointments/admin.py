""" foxtail/appointments/admin.py """
from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """ Admin panel options for the Appointment model. """
    list_display = (
        'name',
        'time_slot',
        'clinic',
        Appointment.get_clinic_date,
        'status',
    )
    list_filter = (
        'status',
        'language',
        'clinic',
    )
    ordering = (
        'time_slot',
        'phone',
    )
