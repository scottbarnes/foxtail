""" foxtail/organizations/tests/test_models.py """
from ..models import Organization

# from factory import DjangoModelFactory, SubFactory
# from faker import Faker


fake = Faker(['en-US', 'ko-KR', 'es_MX'])

class ClinicFactory(DjangoModelFactory):

    def Set
    name = Faker('company')

    class Meta:
        model = Organization
