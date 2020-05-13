""" foxtail/appointments/tests/factories.py """

from factory import DjangoModelFactory, Faker, LazyAttribute, SubFactory
import factory.fuzzy

from ..models import Appointment
from foxtail.clinics.models import TIME_CHOICES
from foxtail.attorneys.tests.factories import AttorneyFactory
from foxtail.clinics.tests.factories import ClinicFactory
from foxtail.organizations.tests.factories import OrganizationFactory


class AppointmentFactory(DjangoModelFactory):
    name = Faker('name')
    time_slot = factory.fuzzy.FuzzyChoice([x[0] for x in TIME_CHOICES])
    phone = Faker('phone_number')
    email = Faker('ascii_safe_email')
    address = Faker('address')
    slug = LazyAttribute(lambda x: x.name)
    description = Faker('paragraphs', nb=3)
    waiver = Faker('file_path', depth=3)
    language = factory.fuzzy.FuzzyChoice([x[0] for x in Appointment.Language.choices])
    status = factory.fuzzy.FuzzyChoice([x[0] for x in Appointment.Status.choices])
    clinic = SubFactory(ClinicFactory)
    attorney = SubFactory(AttorneyFactory)
    organization = SubFactory(OrganizationFactory)

    class Meta:
        model = Appointment
