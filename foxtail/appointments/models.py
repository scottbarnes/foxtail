""" foxtail/appointments/models.py """
from datetime import date as Date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from model_utils import FieldTracker

from autoslug import AutoSlugField
import jwt
from model_utils.models import TimeStampedModel
from time import time

from config.settings.base import env
from foxtail.attorneys.models import Attorney
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
    time_slot = models.CharField('Time slot', max_length=255, blank=True, null=True, choices=TIME_CHOICES)
    phone = models.CharField('Phone', max_length=255)  # Intentionally not validating. Would use libphonenumber.
    email = models.EmailField('Email', max_length=50)  # Validate b/c emails are sent.
    address = models.CharField('Address', max_length=255)  # No validation at all.
    slug = AutoSlugField('Appointment address', unique=True, always_update=False, populate_from='name')
    description = models.TextField('Description')
    # tags  #  TODO: add support for tagging.
    # custom manager # TODO: add custom manager for Status and Language to allow for easier DB queries
    waiver = models.FileField(upload_to='waivers/%Y/%m/', blank=True)
    language = models.CharField('Language', choices=Language.choices, max_length=255)
    # attorney = models.CharField('Attorney', max_length=255, blank=True)
    status = models.CharField('Status', choices=Status.choices, max_length=255, default='waiver-emailed')
    tracker = FieldTracker(fields=['status'])
    # ForeignKeys
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name='appointments')
    attorney = models.ForeignKey(Attorney, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='appointments')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name='appointments')
    # Hidden/excluded fields
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='appointments_created')  # null=True necessary because of SET_NULL.
    # For django-admin-sortable2
    admin_order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        # For django-admin-sortable2
        ordering = ['admin_order']

    def clean(self) -> None:
        # Make sure scheduled clinic and organization match
        if self.clinic.organization != self.organization:
            raise ValidationError({'clinic': 'The scheduled clinic and organization must match.'})
        if self.clinic.date < Date.today():
            raise ValidationError({'clinic': 'The clinic date can\'t be in the past'})

        # Make sure attorney is not already scheduled for this date and time.
        def check_for_double_booked_attorney(attorney):
            """ Check the attorney's schedule to see if he or she is already booked at this date and time. """
            if attorney:  # Check if there are any attorneys; save breaks otherwise.
                # Need to continue if it's checking itself or it will never save.
                this_date = self.clinic.date
                this_time = self.time_slot
                appointments = attorney.appointments.all()  # QuerySet of other appointments.
                for appointment in appointments:
                    if appointment.id == self.id:
                        # Bail on this iteration, otherwise it's impossible to save an existing object b/c it will
                        # always have the same appointment date+time as itself.
                        continue
                    try:
                        if appointment.clinic.date == this_date:
                            if appointment.time_slot == this_time:
                                raise ValidationError({'attorney': f'This attorney is already scheduled with'
                                                                   f' {appointment.name} on {appointment.clinic.date}'
                                                                   f' at {appointment.time_slot}.'})
                    except AttributeError as e:
                        pass

        check_for_double_booked_attorney(self.attorney)

    def get_clinic_date(self) -> str:
        """ Return the date of the clinic in YYYY-MM-DD. """
        try:  # Catch errors from deleted clinics.
            date: str = self.clinic.date.strftime('%Y-%m-%d')
        except AttributeError as e:
            date: str = "Clinic deleted?"
        return date
    get_clinic_date.short_description = 'Date'  # Where in the world is .short_description documented?

    def get_clinic_street_address(self) -> str:
        """
        Return the clinic street address as set... here.
        """
        try:
            address: str = self.organization.location
        except:
            address: str = 'ERROR NO ADDRESS'
        return address

    def get_clinic_phone_number(self) -> str:
        """ Return the clinic phone number. """
        try:
            phone: str = self.organization.phone
        except:
            phone: str = 'ERROR NO PHONE'
        return phone

    def get_waiver_upload_token(self, expires_in=1209600):
        """
        Create a JSON web token to send with the initial email to a client. This token will
        ollow the user to upload the wavier to their Appointment simply by clicking the link.
        """
        return jwt.encode(
            {'upload_waiver': self.id, 'exp': time() + expires_in},
            env('DJANGO_SECRET_KEY'), algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_waiver_upload_token(token):
        """ Verify the JSON web token to allow a user to upload the waiver to their Appointment. """
        try:
            application_id = jwt.decode(token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])['upload_waiver']
        except:
            return
        return Appointment.objects.get(id=application_id)

    def __str__(self):
        return f'{self.name}'

    def get_waiver_absolute_url(self):
        """
        Return the url (including token argument) for the waiver upload.
        There must be a better way to do this. :(
        """
        return reverse('')

    def get_absolute_url(self):
        """ Returns an absolute URL this appointment entry. """
        pass
        # TODO add this once the URL + view are wired
