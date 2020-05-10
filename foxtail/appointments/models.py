""" foxtail/appointments/models.py """
from datetime import date as Date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from model_utils import FieldTracker

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

from config.settings.base import env
from foxtail.clinics.models import Clinic, Organization, TIME_CHOICES


class Appointment(TimeStampedModel):
    """ Clinic appointments. Currently the clinic attendees are not 'users' of the platform. Instead there are
    'clinics' and each clinic has various 'appointments', people's names are just a field of an appointment."""

    class Language(models.TextChoices):
        """ Set the client's language abilities. """
        KOREAN_NEED_INTERPRETER = 'korean-no-interpreter', 'Korean: Need interpreter'
        KOREAN_WITH_INTERPRETER = 'korean-with-interpreter', 'Korean: Bringing interpreter'
        ENGLISH = 'english', 'English: no interpreter needed'

    class Status(models.TextChoices):
        """ Let staff set the status re the waiter and scheduling. """
        WAIVER_EMAILED = 'waiver-emailed', 'Step 1: Pending waiver return'
        WAIVER_SIGNED = 'waiver-signed', 'Step 2: Pending scheduling'
        CONFIRMED = 'confirmed', 'Step 3: Client scheduled'
        CONFIRMED_WITH_ATTORNEY = 'confirmed-with-attorney', 'Step 4: Client AND attorney scheduled'

    name = models.CharField('Name', max_length=255)
    time_slot = models.CharField('Timeslot', max_length=255, blank=True, choices=TIME_CHOICES)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name='appointments')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name='appointments')
    phone = models.CharField('Phone', max_length=255)  # Intentionally not validating. Would use libphonenumber.
    email = models.EmailField('Email', max_length=50)  # Validate b/c emails are sent.
    address = models.CharField('Address', max_length=255)  # No validation at all.
    slug = AutoSlugField('Appointment address', unique=True, always_update=False, populate_from='name')
    description = models.TextField('Description')
    # tags  #  TODO: add support for tagging.
    # custom manager # TODO: add custom manager for Status and Language to allow for easier DB queries
    # organization # TODO: is this needed? Or will the ForeignKey in Clinic the job?
    waiver = models.FileField(upload_to='waivers/%Y/%m/', blank=True)
    language = models.CharField('Language', choices=Language.choices, max_length=255)
    attorney = models.CharField('Attorney', max_length=255, blank=True)
    status = models.CharField('Status', choices=Status.choices, max_length=255, default='waiver-emailed')
    tracker = FieldTracker(fields=['status'])
    # Hidden/excluded fields
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='appointments_created')  # null=True necessary because of SET_NULL.

    def clean(self) -> None:
        # Make sure scheduled clinic and organization match
        if self.clinic.organization != self.organization:
            raise ValidationError({'clinic': 'The scheduled clinic and organization must match.'})
        if self.clinic.date < Date.today():
            raise ValidationError({'clinic': 'The clinic date can\'t be in the past'})

    def get_clinic_date(self) -> str:
        """ Return the date of the clinic in YYYY-MM-DD. """
        return self.clinic.date.strftime('%Y-%m-%d')
    get_clinic_date.short_description = 'Date'  # Where in the world is .short_description documented?

    # def get_clinic_name(self) -> str:
    #     """ Return the clinic's name based on the label of the choice in Clinic.Organizations. """
    #     org: str = self.clinic.organization  # Get organization abbreviation.
    #     clinics: dict = dict(Clinic.Organization.choices)  # List of tuples converted to dictionary.
    #     org: str = clinics[org]
    #     return org

    def get_clinic_street_address(self) -> str:
        """
        Return the clinic street address as set... here.
        TODO: fix the models so this stuff is stored in the clinic model.
        """
        org: str = self.clinic.organization
        if org == 'kaf':
            address: str = '9876 West Garden Grove Blvd, Garden Grove, CA 92844'
        elif org == 'kcs':
            address: str = '8352 Commonwealth Ave., Buena Park, CA 90621'
        else:
            address: str = 'ERROR NO ADDRESS'
        return address

    def get_clinic_phone_number(self) -> str:
        """ Return the clinic phone number. """
        org: str = self.clinic.organization
        if org == 'kaf':
            phone: str = '714-530-4810'
        elif org == 'kcs':
            phone: str = '714-503-6550'
        else:
            phone: str = 'ERROR NO PHONE'
        return phone

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        """ Returns an absolute URL this appointment entry. """
        # TODO add this once the URL + view are wired

