""" foxtail/clinics/tests/test_models.py """
import pytest

from .factories import ClinicFactory

pytestmark = pytest.mark.django_db


def test_get_organization():
    clinic = ClinicFactory()
    org = clinic.organization
    assert clinic.get_organization() == org.name
