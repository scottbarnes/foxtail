""" foxtail/appointments/views.py """
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, UpdateView


from .models import Appointment


def AppointmentWaiverUploadView(request, token):
    appointment = Appointment.verify_waiver_upload_token(token)  # Get the relevant Appointment object instance.
    if not appointment:
        return redirect('home')
    if request.method == 'POST':
        form = AppointmentWaiverUploadForm(request.POST)
        if form.is_valid():
            # process data
            # send a message to the message network
            return redirect('success page wherever that is')
    return render(request, 'appointments/upload_waiver_form.html', {'token': token, 'form': form})


# Later see: https://stackoverflow.com/questions/40250533/the-view-manager-views-login-didnt-return-an-httpresponse-object-it-returned-n?rq=1

#class AppointmentWaiverUploadView(TemplateView):
#    model = Appointment
#    fields = ['waiver']
