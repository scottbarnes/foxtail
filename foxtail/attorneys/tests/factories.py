""" foxtail/attorneys/tests/factories.py """
from ..models import Attorney

from factory import DjangoModelFactory, Faker


class AttorneyFactory(DjangoModelFactory):

    # Faker formatters: https://faker.readthedocs.io/en/master/providers.html
    name = Faker('name')

    class Meta:
        model = Attorney
