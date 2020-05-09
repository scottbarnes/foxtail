""" foxtail/clinics/admin.py """
from django.contrib import admin

from guardian.admin import GuardedModelAdmin, GuardedModelAdminMixin
from guardian.shortcuts import get_objects_for_user, get_objects_for_group

from .models import Clinic
from foxtail.appointments.models import Appointment


class AppointmentInLine(admin.StackedInline):
    """ Edit Appointment instances from within the Clinic admin panel. """
    model = Appointment
    show_change_link = True
    ordering = ('time_slot',)  # Sorts the display of Appointment OBJECTS. Not the contents.


@admin.register(Clinic)
class ClinicAdmin(GuardedModelAdmin):
    """
    This was not at all intuitive to me. To make this work I needed to:
    1. Give the group (e.g. KCS) the relevant permissions globally (/admin/auth/group/<gid>/);
    2. At this point, changing permissions using django-guardian for the object or instance did nothing and users
        could see all objects as usual (which is expected, given that they had global permissions via the group).
    3. To make those object/instance permissions take effect I needed to override get_queryset to use the query
        I wanted (e.g. as below), because for some reason following the example from django-guardian was throwing
        errors. Specifically trying to use group_can_access_owned_by_group_objects_only = True didn't work (though
        user_can_access_owned_objects_only = True did work...).
    Note: the inlines won't display unless access is setup with django-guardian and appropriate permissions.
    """
    def get_queryset(self, request):
        """
        Override... I think... get_queryset to return the query_set of Clinic objects to which the user has access
        (by way of either individual or group permissions).
        """
        qs = super(ClinicAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = get_objects_for_user(request.user, 'view_clinic', klass=Clinic, use_groups=True, accept_global_perms=False)
        return qs
    list_display = (
        'organization',
        'date',
        'start_time',
    )
    inlines = [
        AppointmentInLine
    ]
    ordering = ('date',)  # Sorts the list on the main Clinics page.

