""" foxtail/organizations/models.py """
from django.db import models
from model_utils.models import TimeStampedModel

from autoslug import AutoSlugField


class Organization(TimeStampedModel):
    """ Create an organization instance. """
    name = models.CharField('Organization', max_length=255)
    abbreviation = models.CharField('Organization abbreviation', max_length=10)
    slug = AutoSlugField('Organization link', unique=True, always_update=False, populate_from='name')
    location = models.CharField('Location', max_length=255)
    phone = models.CharField('Phone', max_length=255)
    email = models.EmailField('Email', max_length=30)
    website = models.URLField('Website', max_length=255)
    # clinic is a ForeignKey

    def __str__(self):
        return self.name
