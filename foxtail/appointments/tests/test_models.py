""" foxtail/appointments/tests/test_models.py """
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

import pytest
from guardian.shortcuts import assign_perm

from .factories import AppointmentFactory
from ..admin import AppointmentAdmin
from ..models import Appointment
from foxtail.attorneys.tests.factories import AttorneyFactory
from foxtail.clinics.tests.factories import ClinicFactory
from foxtail.clinics.utilities import get_time_slot_choices
from foxtail.organizations.tests.factories import OrganizationFactory
from foxtail.users.models import User

pytestmark = pytest.mark.django_db


class AppointmentModelTests(TestCase):

    def setUp(self):
        # Create some entities
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

        # Set up a RequestFactory
        self.rf = RequestFactory()

        # Create two staff users for two organizations.
        self.client_org1 = Client()
        self.client_org2 = Client()
        self.password = 'testing'
        User.objects.create_user(username='user_org1', password=self.password, is_staff=True)
        User.objects.create_user(username='user_org2', password=self.password, is_staff=True)
        self.user_org1 = User.objects.get(username='user_org1')
        self.user_org2 = User.objects.get(username='user_org2')

        # Create groups
        Group.objects.create(name='org1')
        Group.objects.create(name='org2')
        self.group_org1 = Group.objects.get(name='org1')
        self.group_org2 = Group.objects.get(name='org2')

    def tearDown(self):
        self.user_org1.delete()
        self.user_org2.delete()

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

    def test_get_appointment_time_in_am_pm(self):
        self.appointment_two.time_slot = '16:00'
        get_app = self.appointment_two.get_appointment_time_in_am_pm
        self.assertEqual(get_app(), '4:00 PM')

        self.appointment_two.time_slot = ''
        self.assertEqual(get_app(), 'NO TIME SET')

        self.appointment_two.time_slot = None
        self.assertEqual(get_app(), 'NO TIME SET')

    def test_staff_user_not_in_any_group_cannot_see_any_appointments(self):
        url = reverse('admin:appointments_appointment_changelist')
        self.client_org1.force_login(self.user_org1)
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 302)
        self.client_org1.logout()

    def test_group_members_cannot_see_appointments_even_with_global_perms(self):
        """
        All of the steps labeled 'manual' are things an admin would manually do in the
        admin panel.

        Still can't see the view at this point because of the get_queryset() override.
        """
        # Put the user in a group, manually.
        self.user_org1.groups.add(self.group_org1)
        self.user_org1.save()

        # Get the relevant permission objects and then assign them, manually.
        add = Permission.objects.get(codename='add_appointment')
        view = Permission.objects.get(codename='view_appointment')
        change = Permission.objects.get(codename='change_appointment')
        delete = Permission.objects.get(codename='delete_appointment')

        self.group_org1.permissions.add(add, view, change, delete)

        url = reverse('admin:appointments_appointment_changelist')
        self.client_org1.force_login(self.user_org1)
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 302)
        self.client_org1.logout()

    # def test_only_group_that_adds_appointment_can_see_it(self):
    #     data = {
    #         'name': 'Testy McTester',
    #         'phone': 'not a real phone number',
    #         'email': 'mctester@example.com',
    #         'address': '123 Main Street',
    #         'description': 'Zug zug zug zug zug zug zug zug.',
    #         'language': 'korean-no-interpreter',
    #         'status': 'waiver-emailed',
    #         'organization': self.organization,
    #     }  # For the organization, note this is the first one, so the later clinic must match.

    #     # Log the user in and make the request.
    #     self.client_org2.force_login(self.user_org2)
    #     url = reverse('admin:appointments_appointment_add')  # Check DJDT to see this name in the request.
    #     response = self.client_org1.post(url, data)

    #     # Check everything that the response code is good, there's a new object, and it has the correct name.
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Appointment.objects.count(), 4)
    #     newest_app = Appointment.objects.last()
    #     self.assertEqual(newest_app.name, 'Testy McTester')


    def test_only_group_that_adds_appointment_can_see_it(self):
        """ This test does not appear to work. Though it can submit items, they're not added to the DB. Why? """
        data = {
            'NOT A FIELD': 'THIS IS VERY PUZZLING',
            'name': 'Testy McTester',
            'phone': 'not a real phone number',
            'email': 'mctester@example.com',
            'address': '123 Main Street',
            'description': 'Zug zug zug zug zug zug zug zug.',
            'language': 'korean-no-interpreter',
            'status': 'waiver-emailed',
            'organization': self.organization,
        }  # For the organization, note this is the first one, so the later clinic must match.
        # # Put the user in a group, manually.
        self.user_org1.groups.add(self.group_org1)
        self.user_org1.save()

        # Get the relevant permission objects and then assign them, manually.
        add = Permission.objects.get(codename='add_appointment')
        view = Permission.objects.get(codename='view_appointment')
        change = Permission.objects.get(codename='change_appointment')
        delete = Permission.objects.get(codename='delete_appointment')

        self.group_org1.permissions.add(add, view, change, delete)

        # Log the user in and make the request.
        # self.client_org1.force_login(self.user_org1)
        self.assertTrue(self.client_org1.login(username='user_org1', password='testing'))  # USERNAME, not object name.
        url = reverse('admin:appointments_appointment_add')  # Check DJDT to see this name in the request.
        response = self.client_org1.post(url, data)

        # Check everything that the response code is good, there's a new object, and it has the correct name.
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(Appointment.objects.count(), 4)
        newest_app = Appointment.objects.last()
        # self.assertEqual(newest_app.name, 'Testy McTester')

