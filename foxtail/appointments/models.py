""" foxtail/appointments/models.py """
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

from foxtail.clinics.models import Clinic


class Appointment(TimeStampedModel):
    """ Clinic appointments. Currently the clinic attendees are not 'users' of the platform. Instead there are
    'clinics' and each clinic has various 'appointments', people's names are just a field of an appointment."""
    name = models.CharField('Name', max_length=255)
    phone = models.CharField('Phone', max_length=255)  # Intentionally not validating. Would use libphonenumber.
    email = models.EmailField('Email', max_length=50)  # Validate b/c emails are sent.
    slug = AutoSlugField('Appointment address', unique=True, always_update=False, populate_from='name')
    description = models.TextField('Description')
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name='appointments')
    time_slot = models.CharField('Timeslot', max_length=255, blank=True)
    # tags  #  TODO: add support for tagging.
    # custom manager # TODO: add custom manager for Status and Language to allow for easier DB queries
    # organization # TODO: is this needed? Or will the ForeignKey in Clinic the job?
    waiver = models.FileField(upload_to='waivers/%Y/%m/', blank=True)

    class Status(models.TextChoices):
        """ Let staff set the status re the waiter and scheduling. """
        WAIVER_EMAILED = 'waiver-emailed', 'Pending: waiver emailed to client (waiting on client)'
        WAIVER_SIGNED = 'waiver-signed', 'Pending: waiver signed and returned (awaiting scheduling)'
        CONFIRMED = 'confirmed', 'Confirmed: client scheduled'

    status = models.CharField('Status', choices=Status.choices, max_length=255)

    class Language(models.TextChoices):
        """ Set the client's language abilities. """
        KOREAN_NEED_INTERPRETER = 'korean-no-interpreter', 'Mono-lingual Korean: need interpreter'
        KOREAN_WITH_INTERPRETER = 'korean-with-interpreter', 'Mono-lingual Korean: bringing own interpreter'
        ENGLISH = 'english', 'English: no interpreter needed'

    language = models.CharField('Language', choices=Language.choices, max_length=255)

    def get_absolute_url(self):
        """ Returns an absolute URL this appointment entry. """
        # TODO add this once the URL + view are wired

    def __str__(self):
        return f'{self.name}'
