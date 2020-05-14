{% extends 'mail_templated/base.tpl' %}

{% block subject %}
    Reminder of your legal clinic appointment at {{ appointment.time_slot }} on
    {{ appoinment.clinic.date|date:'l, F m' }}
{% endblock subject %}

{% block body %}
    {% with clinic_name=appointment.organization %}
        We've found an attorney who can give you a pro bono advisory consultation.

        You've been scheduled for the {{ clinic_name }} pro bono legal clinic as follows:
        {% comment %}
        See https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#std:templatefilter-date for date filter.
        {% endcomment %}
        Date: {{ appointment.clinic.date|date:'l, F m, Y' }}
        Time: {{ appointment.time_slot }}
        Location: {{ appointment.get_clinic_street_address }}
        Phone: {{ appointment.get_clinic_phone_number }}

        PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have questions
        about your clinic appointment, please contact {{ clinic_name }} at {{ appointment.get_clinic_phone_number }}.
    {% endwith %}
{% endblock body %}

{% block html %}
    {% with clinic_name=appointment.get_clinic_name %}
        <p>We've found an attorney who can give you a pro bono advisory consultation.</p>

        <p>
            You've been scheduled for the {{ clinic_name }} pro bono legal clinic as follows:
            {% comment %}
            See https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#std:templatefilter-date for date filter.
            {% endcomment %}
            Date: {{ appointment.clinic.date|date:'l, F m, Y' }}
            Time: {{ appointment.time_slot }}
            Location: {{ appointment.get_clinic_street_address }}
            Phone: {{ appointment.get_clinic_phone_number }}
        </p>

        <p>
            PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have
            questions about your clinic appointment, please contact {{ clinic_name }} at
            {{ appointment.get_clinic_phone_number }}.
        </p>
    {% endwith %}
{% endblock html %}
