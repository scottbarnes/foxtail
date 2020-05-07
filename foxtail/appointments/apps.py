""" foxtail/appointments/apps.py """
from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    name = 'foxtail.appointments'

    def ready(self):
        """ Register the signal handlers in appointments.signals.handlers.py. """
        import foxtail.appointments.signals.handlers  #noqa
