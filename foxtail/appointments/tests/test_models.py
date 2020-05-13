""" foxtail/appointments/tests/test_models.py """
from django.core.exceptions import ValidationError
from django.test import TestCase
import pytest

from .factories import AppointmentFactory
from foxtail.clinics.tests.factories import ClinicFactory
from foxtail.attorneys.tests.factories import AttorneyFactory

pytestmark = pytest.mark.django_db


class AppointmentModelTests(TestCase):

    def setUp(self):
        self.appointment = AppointmentFactory()
        self.clinic = self.appointment.clinic
        self.organization = self.appointment.organization
        self.attorney = self.appointment.attorney

    def test_clean(self):
        self.organization = 'SOME OTHER ORGANIZATION THAN THE ONE FROM THE CLINIC'
        self.assertRaises(ValidationError, self.appointment.full_clean)

