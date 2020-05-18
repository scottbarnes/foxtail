""" foxtail/organizations/admin.py """
from django.contrib import admin, messages

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(GuardedModelAdmin):
    """ Admin panel options for the Organization model. """
    # model = Organization
    def get_queryset(self, request):
        """
        Override get_queryset so that staff users see only objects which their group is
        allowed to see.

        Specifically, accept_global_perms=False is what stops the staff users from seeing
        other organizations, as for some reason staff users still need global permissions
        to see things in the admin panel, even when their group permissions should allow
        them to see without global permissions. Or at least that is happening with the
        current setup.
        """
        qs = super(OrganizationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = get_objects_for_user(request.user, 'view_organization', klass=Organization,
                                  use_groups=True, accept_global_perms=False)
        return qs

    def save_model(self, request, obj, form, change):
        """
        Override save to send a message about the steps after creating a new organization.
        They boil down to:
        1. Adding a new group for that organization: /admin/auth/group/
        2. Giving that group view+change permissions for organizations.
        3. Adding users for the group: /admin/users/user/
        4. Adding users TO the group.
        """
        if obj.id is None:  # Only send messages with new objects.
            messages.add_message(request, messages.WARNING, 'Don\'t forget to add users to your group')
        # Don't forget to save.
        super(OrganizationAdmin, self).save_model(self, obj, form, change)
