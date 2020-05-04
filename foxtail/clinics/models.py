""" foxtail/clinics/models.py """
from django.db import models
from model_utils.models import TimeStampedModel


class Clinic(TimeStampedModel):
    """ Make clinic instances. """
    class Organization(models.TextChoices):
        """ Set the organizations. """
        KCS = 'kcs', 'Korean Community Services (KCS)'
        KAF = 'kaf', 'Korean American Federation (KAF)'
    organization = models.CharField('Organization', max_length=50, choices=Organization.choices)
    date = models.DateField('Date')
    start_time = models.TimeField('Start time')  # Validate in form. :(
    end_time = models.TimeField('End time')  # Validate in form. :(
    # Appointments are from a ForeignKey out of appointments/models.py

    def __str__(self):
        return f'Organization: {self.organization.upper()}, Date: {self.date}'


