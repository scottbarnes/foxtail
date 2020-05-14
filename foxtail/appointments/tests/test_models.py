""" foxtail/appointments/tests/test_models.py """
from django.core.exceptions import ValidationError
from django.test import TestCase
import pytest

from .factories import AppointmentFactory
from ..models import Appointment
from foxtail.attorneys.tests.factories import AttorneyFactory
from foxtail.clinics.tests.factories import ClinicFactory
from foxtail.organizations.tests.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


class AppointmentModelTests(TestCase):

    def setUp(self):
        self.clinic = ClinicFactory()  # This makes the organization too.
        self.organization = self.clinic.organization
        self.attorney = AttorneyFactory()
        self.appointment = AppointmentFactory(
            organization=self.organization,
            attorney=self.attorney,
            clinic=self.clinic,
        )
        self.clinic_two = ClinicFactory()  # This makes the organization too.
        self.organization_two = self.clinic_two.organization
        self.attorney_two = AttorneyFactory()
        self.appointment_two = AppointmentFactory(
            organization=self.organization_two,
            attorney=self.attorney_two,
            clinic=self.clinic_two,
        )
        self.clinic_three = ClinicFactory()  # This makes the organization too.
        self.organization_three = self.clinic_three.organization
        self.attorney_three = AttorneyFactory()
        self.appointment_three = AppointmentFactory(
            organization=self.organization_three,
            attorney=self.attorney_three,
            clinic=self.appointment_two.clinic,  # Get the clinic date from appointment_two. For double booking.
            time_slot=self.appointment_two.time_slot,  # And the time slot.
        )


    def test_clean_same_organizations(self):
        # Very a full clean works with the two organizations as the same
        self.assertEqual(self.appointment.organization, self.clinic.organization)
        self.appointment.full_clean()

    def test_clean_different_organizations(self):
        # Raise a validation error if a different organization 'owns' the client than holds the clinic.
        self.appointment.organization = OrganizationFactory()
        # Need to use a context manager b/c error is raised before self.assertRaises would otherwise be evaluated.
        with self.assertRaises(ValidationError):
            self.appointment.full_clean()
        self.appointment.organization = self.organization  # Put things back how they were.

    def test_clean_double_booking(self):
        # Ensure the two appointments have different IDs from each other.
        self.assertEqual(self.appointment_two.clinic.date, self.appointment_three.clinic.date)
        self.assertEqual(self.appointment_two.time_slot, self.appointment_three.time_slot)
        # Test for attorney double bookings.
        with self.assertRaises(ValidationError):
            self.appointment_three.full_clean()

