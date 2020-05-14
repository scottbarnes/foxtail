""" foxtail/appointments/tasks.py """
from datetime import date, timedelta

from config import celery_app
from config.settings.base import APPS_DIR
from mail_templated import send_mail

from .models import Appointment


@celery_app.task()
def send_two_day_appointment_reminders():
    """ Get appointments two days hence. Returns a QuerySet. """
    # Get the appointments as a QuerySet.
    now = date.today()
    two_days_from_now = now + timedelta(days=2)
    appointments = Appointment.objects.filter(clinic__date=two_days_from_now)

    # If there are any appointments, send out reminders.
    if appointments:
        # Set the 'from' email once. But send individual emails. Hopefully this helps reduce spam flagging.
        from_email = 'Pro bono clinic <oclegalclinic@gmail.com>'
        for appointment in appointments:
            # Set the 'to' email each time.
            to_email = appointment.email
            send_mail(APPS_DIR / 'templates/appointments/emails/reminder.tpl',
                      {'appointment': appointment},
                      from_email,
                      [to_email]
                    )



