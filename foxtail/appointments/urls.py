""" foxtail/appointments/urls.py """
from django.urls import path

from foxtail.appointments.views import (
    AppointmentWaiverUploadView,
)

app_name = "appointments"
urlpatterns = [
    # Matches will call appointment_waiver_upload with token = str (i.e. the token itself).
    # I NEED TO DO A REDIRECT VIEW PROBABLY, OR SOME OTHER VIEW, WHERE I VERIFY THE JWT
    # AND THEN ON SUCCESS REDIRECT TO THE APPROPRIATE OBJECT PK UPLOAD_WAIVER VIEW.
    # path("upload_waiver/<str:token>/", view=AppointmentWaiverUploadView.as_view, name="appointment_waiver_upload"),
    path("upload_waiver/<str:token>", view=AppointmentWaiverUploadView, name="appointment_waiver_upload"),
    # path("upload_waiver/<int:pk>", view=AppointmentWaiverUploadView.as_view(), name="appointment_waiver_upload"),
]
