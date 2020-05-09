""" foxtail/clinics/admin.py """
from django.contrib import admin, messages

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, get_objects_for_user

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
    1. Give the group (e.g. KCS) the relevant permissions (CRUD, but specifically Change) globally by visiting
        localhost:8000/admin/auth/group/<gid>/; by default view_<model>, change_<model> etc. exist. Per
        https://django-guardian.readthedocs.io/en/stable/userguide/assign.html.
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

    def save_model(self, request, obj, form, change):
        """
        For reasons that are beyond me, saving the object from the admin panel didn't save the User object. This
        overrides save to get the user from request, to which the Admin models have access.

        Use assign_perm from django-admin to give the creator's group permissions to the object instance. If the creator
        does not have only one group, presumably the person is an admin. Use the messages framework to flash a WARNING
        if when this happens to alert the admin to set the permissions manually.
        """
        obj.created_by = request.user
        super(ClinicAdmin, self).save_model(request, obj, form, change)
        # With the object persisted, permissions can now be granted.
        creator = obj.created_by
        if creator.groups.count() != 1:
            messages.add_message(request, messages.WARNING, 'Remember: until you you chang this clinic\'s object'
                                                            ' permissions, no organization can see it.')
        else:
            group = creator.groups.first()
            assign_perm('change_clinic', group, obj)
            assign_perm('view_clinic', group, obj)
            assign_perm('delete_clinic', group, obj)

    list_display = (
        'organization',
        'date',
        'start_time',
    )
    list_filter = (
        'organization',
    )
    exclude = ['created_by']
    inlines = [
        AppointmentInLine
    ]
    ordering = ('-date',)  # Sorts the list on the main Clinics page in reverse chronological order.
