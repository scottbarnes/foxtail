""" foxtail/clinics/models.py """
from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel

from guardian.shortcuts import get_objects_for_group

from foxtail.organizations.models import Organization
from foxtail.users.models import User


TIME_CHOICES = (('07:00:00', '7:00 AM'), ('07:30:00', '7:30 AM'), ('08:00:00', '8:00 AM'), ('08:30:00', '8:30 AM'),
                ('09:00:00', '9:00 AM'), ('09:30:00', '9:30 AM'), ('10:00:00', '10:00 AM'), ('10:30:00', '10:30 AM'),
                ('11:00:00', '11:00 AM'), ('11:30:00', '11:30 AM'), ('12:00:00', 'Noon'), ('12:30:00', '12:30 PM'),
                ('13:00:00', '1:00 PM'), ('13:30:00', '1:30 PM'), ('14:00:00', '2:00 PM'), ('14:30:00', '2:30 PM'),
                ('15:00:00', '3:00 PM'), ('15:30:00', '3:30 PM'), ('16:00:00', '4:00 PM'), ('16:30:00', '4:30 PM'),
                ('17:00:00', '5:00 PM'), ('17:30:00', '5:30 PM'), ('18:00:00', '6:00 PM'), ('18:30:00', '6:30 PM'),
                ('19:00:00', '7:00 PM'), ('19:30:00', '7:30 PM'), ('20:00:00', '8:00 PM'), ('20:30:00', '8:30 PM'),
                ('21:30:00', '9:00 PM'), ('21:00:00', '9:30 PM'),)


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
        return f'{self.organization.abbreviation}'


