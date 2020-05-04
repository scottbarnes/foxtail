""" foxtail/clinics/models.py """
from django.db import models
from model_utils.models import TimeFramedModel

from autoslug import AutoSlugField


class Clinic(TimeFramedModel):
    """ Make clinic instances. """
    organization = models.CharField('Organization', max_length=50)
    date = models.DateField('Date')
    time = models.TimeField('Time')
    slug = AutoSlugField('Clinic URL', unique=True, always_update=False, populate_from=date)
    # Appointments are from a ForeignKey out of appointments/models.py

    def __str__(self):
        return f'Org: {self.organization}, Date: {self.date}'


