""" foxtail/appointments/signals/handlers.py """
# from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from mail_templated import send_mail

from config.settings.base import APPS_DIR
from foxtail.appointments.models import Appointment
# from config.settings.production import DEFAULT_FROM_EMAIL


@receiver(post_save, sender=Appointment)
def appointment_status_update_emails(sender, instance, created, **kwargs):
    """
    Send email to a client on three appointment related conditions:
     1. The Appointment object is first created - let client know they need to sign the waiver;
     2. The status is changed to waiver-signed - let client know they'll be informed if they're scheduled;
     3. The status is changed to confirmed - let client know date, time, location of the clinic.

    This is probably functionally identical to overriding save(). Use FieldTracker to send email _only_ when
    the status actually changes. Not just when there's a .save() and when a status matches a criterion.

    Note: this handler is registered in foxtail/appointments/apps.py using ready().
    Per https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
    """

    from_email = 'Pro bono clinic <oclegalclinic@gmail.com>'
    to_email = instance.email

    if created:  # only True when object first created.
        token = instance.get_waiver_upload_token()  # Generate the waiver_upload token with the Application method.
        send_mail(APPS_DIR / 'templates/appointments/emails/appointment-creation.tpl',
                  {'appointment': instance, 'token': token},
                  from_email,
                  [to_email]
                  )

    elif instance.tracker.has_changed('status'):
        """
        Evaluates to True when the tracked status field in question has changed.
        See https://django-model-utils.readthedocs.io/en/latest/utilities.html#field-tracker
        """

        if instance.status == 'waiver-signed':
            """
            Send client an email letting him or her know if an attorney is found they will be emailed
            the date and time of the clinic.
            """
            send_mail(APPS_DIR / 'templates/appointments/emails/waiver-signed.tpl',
                      {'appointment': instance},
                      from_email,
                      [to_email]
                      )

        elif instance.status == 'confirmed':
            """
            Email client informing him or her of the appointment date, time, and location.
            """
            send_mail(APPS_DIR / 'templates/appointments/emails/confirmed.tpl',
                      {'appointment': instance},
                      from_email,
                      [to_email]
                      )

