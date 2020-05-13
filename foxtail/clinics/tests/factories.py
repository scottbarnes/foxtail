""" foxtail/clinics/tests/factories.py """

from factory import DjangoModelFactory, Faker, LazyAttribute, SubFactory
import factory.fuzzy

from ..models import Clinic
from foxtail.clinics.models import TIME_CHOICES
from foxtail.organizations.tests.factories import OrganizationFactory


def add_two_hours_to_clinic(start):
    """
    This doesn't work.

    Add two hours to the clinic time so the end is always two hours after the start. Only works with 24 hour
    time with clinics starting no later than 22:00.
    """
    hour, minute = start.split('a')  # Unpack into hour, minute.
    hour = int(hour)
    hour += 2
    hour = str(hour)
    end = hour + ':' + minute
    return end


class ClinicFactory(DjangoModelFactory):
    organization = SubFactory(OrganizationFactory)
    date = Faker('future_date')
    start_time = factory.fuzzy.FuzzyChoice(
        [x[0] for x in TIME_CHOICES]
    )
    end_time = factory.fuzzy.FuzzyChoice(
        [x[0] for x in TIME_CHOICES]
    )
    # end_time = LazyAttribute(lambda x: add_two_hours_to_clinic(x.start_time))

    class Meta:
        model = Clinic
