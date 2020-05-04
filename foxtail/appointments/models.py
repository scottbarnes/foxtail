""" foxtail/appointments/models.py """
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

from foxtail.clinics.models import Clinic

TIME_CHOICES = (('07:00:00', '7:00 AM'),
                ('07:30:00', '7:30 AM'),
                ('08:00:00', '8:00 AM'),
                ('08:30:00', '8:30 AM'),
                ('09:00:00', '9:00 AM'),
                ('09:30:00', '9:30 AM'),
                ('10:00:00', '10:00 AM'),
                ('10:30:00', '10:30 AM'),
                ('11:00:00', '11:00 AM'),
                ('11:30:00', '11:30 AM'),
                ('12:00:00', 'Noon'),
                ('12:30:00', '12:30 PM'),
                ('13:00:00', '1:00 PM'),
                ('13:30:00', '1:30 PM'),
                ('14:00:00', '2:00 PM'),
                ('14:30:00', '2:30 PM'),
                ('15:00:00', '3:00 PM'),
                ('15:30:00', '3:30 PM'),
                ('16:00:00', '4:00 PM'),
                ('16:30:00', '4:30 PM'),
                ('17:00:00', '5:00 PM'),
                ('17:30:00', '5:30 PM'),
                ('18:00:00', '6:00 PM'),
                ('18:30:00', '6:30 PM'),
                ('19:00:00', '7:00 PM'),
                ('19:30:00', '7:30 PM'),
                ('20:00:00', '8:00 PM'),
                ('20:30:00', '8:30 PM'),
                ('21:30:00', '9:00 PM'),
                ('21:00:00', '9:30 PM'),)

class Appointment(TimeStampedModel):
    """ Clinic appointments. Currently the clinic attendees are not 'users' of the platform. Instead there are
    'clinics' and each clinic has various 'appointments', people's names are just a field of an appointment."""
    time_slot = models.CharField('Timeslot', max_length=255, blank=True, choices=TIME_CHOICES)
    name = models.CharField('Name', max_length=255)
    phone = models.CharField('Phone', max_length=255)  # Intentionally not validating. Would use libphonenumber.
    email = models.EmailField('Email', max_length=50)  # Validate b/c emails are sent.
    slug = AutoSlugField('Appointment address', unique=True, always_update=False, populate_from='name')
    description = models.TextField('Description')
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name='appointments')
    # tags  #  TODO: add support for tagging.
    # custom manager # TODO: add custom manager for Status and Language to allow for easier DB queries
    # organization # TODO: is this needed? Or will the ForeignKey in Clinic the job?
    waiver = models.FileField(upload_to='waivers/%Y/%m/', blank=True)

    class Status(models.TextChoices):
        """ Let staff set the status re the waiter and scheduling. """
        WAIVER_EMAILED = 'waiver-emailed', 'Pending: waiver emailed to client (waiting on client)'
        WAIVER_SIGNED = 'waiver-signed', 'Pending: waiver signed and returned (awaiting scheduling)'
        CONFIRMED = 'confirmed', 'Confirmed: client scheduled'

    status = models.CharField('Status', choices=Status.choices, max_length=255, blank=True)

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
