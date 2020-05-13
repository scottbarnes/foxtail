""" foxtail/organizations/tests/factories.py """
from ..models import Organization

# from factory import DjangoModelFactory, SubFactory
# from faker import Faker
from factory import DjangoModelFactory, Faker, LazyAttribute


class OrganizationFactory(DjangoModelFactory):

    # Faker formatters: https://faker.readthedocs.io/en/master/providers.html
    name = Faker('company')
    abbreviation = Faker('country_code')  # This won't match the name, but whatever.
    slug = LazyAttribute(lambda x: x.name)
    location = Faker('address')
    phone = Faker('phone_number')
    email = Faker('company_email')
    website = Faker('domain_name')

    class Meta:
        model = Organization
