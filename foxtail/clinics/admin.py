""" foxtail/clinics/admin.py """
from django.contrib import admin

from .models import Clinic
from foxtail.appointments.models import Appointment


class AppointmentInLine(admin.StackedInline):
    """ Edit Appointment instances from within the Clinic admin panel. """
    model = Appointment
    show_change_link = True
    ordering = ('time_slot',)  # Sorts the display of Appointment OBJECTS. Not the contents.


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    """ Admin panel options for the Clinic model. """
    list_display = (
        'organization',
        'date',
        'start_time'
    )
    inlines = [
        AppointmentInLine
    ]
    ordering = ('date',)  # Sorts the list on the main Clinics page.

