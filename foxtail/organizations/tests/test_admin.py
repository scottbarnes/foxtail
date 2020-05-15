""" foxtail/organizations/tests/test_admin.py """
from django.test import Client, TestCase
import pytest

from .factories import OrganizationFactory
from foxtail.users.models import User


class OrganizationAdminTests(TestCase):

    def setUp(self):
        # Create two staff users for two organizations.
        self.client_ORG1 = Client()
        self.client_ORG2 = Client()
        User.objects.create_user(username='ORG1_user', password='testing', is_staff=True)
        User.objects.create_user(username='ORG2_user', password='testing', is_staff=True)
        self.ORG1_user = User.objects.get(username='ORG1_user')
        self.ORG2_user = User.objects.get(username='ORG2_user')


    def test_clinic_staff_cannot_view_organizations(self):
        # Ensure by default clinic staff can't view organizations.
        self.client_ORG1.force_login(self.ORG1_user)
        response = self.client_ORG1.post('/admin/organizations/organization/')
        self.assertEqual(response.status_code, 403)

