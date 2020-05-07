""" foxtail/appointments/signals/handlers.py """
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    if created:  # only True when object first created.
        send_mail(
            'Triggered by post_save(): ON CREATION',
            'Put the emails elsewhere',
            'DEFAULT_FROM_EMAIL',
            [f'{instance.name} <{instance.email}>'],
            fail_silently=False,
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
            send_mail(
                'Triggered by post_save(): on change to waiver-signed',
                'Triggered on change.',
                'DEFAULT_FROM_EMAIL',
                [f'{instance.name} <{instance.email}>'],
                fail_silently=False,
            )

        elif instance.status == 'confirmed':
            """
            Email client informing him or her of the appointment date, time, and location.
            """
            send_mail(
                'Triggered by post_save(): on change to confirmed',
                'Triggered on change.',
                'DEFAULT_FROM_EMAIL',
                [f'{instance.name} <{instance.email}>'],
                fail_silently=False,
            )

