""" foxtail/attorneys/admin.py """
from django.contrib import admin


from .models import Attorney


@admin.register(Attorney)
class AttorneyAdmin(admin.ModelAdmin):

    exclude = ['created_by']
    # search_fields = ['name']

    def save_model(self, request, obj, form, change):
        """
        For reasons that are beyond me, saving the object from the admin panel didn't save the User object. This
        overrides save to get the user from request, to which the Admin models have access.
        """
        obj.created_by = request.user
        super(AttorneyAdmin, self).save_model(request, obj, form, change)

