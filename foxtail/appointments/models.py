""" foxtail/appointments/models.py """
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

from foxtail.clinics.models import Clinic, TIME_CHOICES


class Appointment(TimeStampedModel):
    """ Clinic appointments. Currently the clinic attendees are not 'users' of the platform. Instead there are
    'clinics' and each clinic has various 'appointments', people's names are just a field of an appointment."""
    time_slot = models.CharField('Timeslot', max_length=255, blank=True, choices=TIME_CHOICES)
    name = models.CharField('Name', max_length=255)
    phone = models.CharField('Phone', max_length=255)  # Intentionally not validating. Would use libphonenumber.
    email = models.EmailField('Email', max_length=50)  # Validate b/c emails are sent.
    address = models.CharField('Address', max_length=255)  # No validation at all.
    slug = AutoSlugField('Appointment address', unique=True, always_update=False, populate_from='name')
    description = models.TextField('Description')
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name='appointments')
    # tags  #  TODO: add support for tagging.
    # custom manager # TODO: add custom manager for Status and Language to allow for easier DB queries
    # organization # TODO: is this needed? Or will the ForeignKey in Clinic the job?
    waiver = models.FileField(upload_to='waivers/%Y/%m/', blank=True)

    class Language(models.TextChoices):
        """ Set the client's language abilities. """
        KOREAN_NEED_INTERPRETER = 'korean-no-interpreter', 'Korean: Need interpreter'
        KOREAN_WITH_INTERPRETER = 'korean-with-interpreter', 'Korean: Bringing interpreter'
        ENGLISH = 'english', 'English: no interpreter needed'

    language = models.CharField('Language', choices=Language.choices, max_length=255)
    attorney = models.CharField('Attorney', max_length=255, blank=True)

    class Status(models.TextChoices):
        """ Let staff set the status re the waiter and scheduling. """
        WAIVER_EMAILED = 'waiver-emailed', 'Step 1: Pending waiver return'
        WAIVER_SIGNED = 'waiver-signed', 'Step 2: Pending scheduling'
        CONFIRMED = 'confirmed', 'Step 3: Client scheduled'
        CONFIRMED_WITH_ATTORNEY = 'confirmed-with-attorney', 'Step 4: Client AND attorney scheduled'

    status = models.CharField('Status', choices=Status.choices, max_length=255, default='waiver-emailed')

    def get_absolute_url(self):
        """ Returns an absolute URL this appointment entry. """
        # TODO add this once the URL + view are wired

    def __str__(self):
        return f'{self.name}'
