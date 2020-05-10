""" foxtail/clinics/models.py """
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel

from guardian.shortcuts import get_objects_for_group

from foxtail.organizations.models import Organization
from foxtail.users.models import User
from .utilities import get_time_slot_choices


# Start and end times, in 24 hour format, for clinic time slot generation.
# Note, if the delta is changed here, it must be changed in appointments/models.py too.
start = datetime(1, 1, 1, 7, 0)
end = datetime(1, 1, 1, 21, 0)
delta = 30
TIME_CHOICES = get_time_slot_choices(start, end, delta)


class Clinic(TimeStampedModel):
    """ Make clinic instances. """
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name='clinics')
    date = models.DateField('Date')
    start_time = models.CharField('Start time', max_length=255, choices=TIME_CHOICES)
    end_time = models.CharField('End time', max_length=255, choices=TIME_CHOICES)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='clinics_created')  # null=True necessary because of SET_NULL.

    def get_organization(self):
        # This should return the organization name for the clinic. Needs testing.
        return self.organization.name

    def __str__(self):
        return f'{self.organization.abbreviation}: {self.date}'


