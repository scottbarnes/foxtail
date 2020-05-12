""" foxtail/attorneys.models.py """
from django.contrib.auth import get_user_model
from django.db import models

from model_utils.models import TimeStampedModel


class Attorney(TimeStampedModel):
    """ Create attorneys so clients can be slotted into them for each Clinic. """
    name = models.CharField('Name', max_length=255)
    # Hidden/excluded fields
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='attorneys_created')  # null=True necessary because of SET_NULL.

    def __str__(self):
        return self.name
