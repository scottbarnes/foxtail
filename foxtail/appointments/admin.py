""" foxtail/appointments/admin.py """
from django import forms
from django.contrib import admin, messages

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm, get_objects_for_user, get_groups_with_perms

from .models import Appointment


# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#
#     def clean(self):
#         """ Custom validation. """
#         clinic = self.cleaned_data.get('clinic')
#
#         return


@admin.register(Appointment)
class AppointmentAdmin(GuardedModelAdmin):
    """
    Admin panel options for the Appointment model.
    See foxtail/clinic/admin.py for notes on struggles with django-guardian.
    """
    def get_queryset(self, request):
        """
        Override... I think... get_queryset to return the query_set of Clinic objects to which the user has access
        (by way of either individual or group permissions).
        """
        qs = super(AppointmentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = get_objects_for_user(request.user, 'view_appointment', klass=Appointment, use_groups=True,
                                  accept_global_perms=False)
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
        super(AppointmentAdmin, self).save_model(request, obj, form, change)
        # With the object persisted, permissions can now be granted.
        creator = obj.created_by
        if creator.groups.count() != 1:
            if not get_groups_with_perms(obj):
                messages.add_message(request, messages.WARNING, 'Remember: until you you change this APPOINTMENT\'S '
                                                                'object permissions, no organization can see it.')
        else:
            group = creator.groups.first()
            assign_perm('change_appointment', group, obj)
            assign_perm('view_appointment', group, obj)
            assign_perm('delete_appointment', group, obj)

    list_display = (
        'name',
        'time_slot',
        'organization',
        Appointment.get_clinic_date,
        'status',
    )
    list_filter = (
        'status',
        'language',
        'organization',
    )
    ordering = (
        'time_slot',
        'phone',
    )
    exclude = ['created_by']
    # autocomplete_fields = ['attorney']
