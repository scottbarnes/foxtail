""" foxtail/clinics/tests/test_models.py """

from ..models import Clinic

from factory import DjangoModelFactory, Faker, SubFactory


class ClinicFactory(DjangoModelFactory):
    organization = SubFactory(OrganizationFactory)  # Maybe.. this needs to be done first.

    class Meta:
        model = Clinic
