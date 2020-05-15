{% extends 'mail_templated/base.tpl' %}
{% comment %}
This is called from foxtail/appointments/tasks.py
{% endcomment %}

{% block subject %}
Reminder: legal clinic appointment at {{ appointment.get_appointment_time_in_am_pm }} on {{ appoinment.clinic.date|date:'l, F m' }}
{% endblock subject %}

{% block body %}
    {% with clinic_name=appointment.organization %}
        As a reminder, you have a legal clinic appointment scheduled with {{ clinic_name }} in two days as follows:
        Date: {{ appointment.clinic.date|date:'l, F m, Y' }}
        Time: {{ appointment.get_appointment_time_in_am_pm }}
        Location: {{ appointment.get_clinic_street_address }}
        Phone: {{ appointment.get_clinic_phone_number }}

        If you *cannot* make the clinic appointment, please contact the organization to let them know so someone else
        can be scheduled instead.

        PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have questions
        about your clinic appointment, please contact {{ clinic_name }} at {{ appointment.get_clinic_phone_number }}.
    {% endwith %}
{% endblock %}

{% block html %}
    {% with clinic_name=appointment.get_clinic_name %}
        <p>As a reminder, you have a legal clinic appointment scheduled with {{ clinic_name }} in two days as follows:</p>
        <p>
            Date: {{ appointment.clinic.date|date:'l, F m, Y' }}
            Time: {{ appointment.get_appointment_time_in_am_pm }}
            Location: {{ appointment.get_clinic_street_address }}
            Phone: {{ appointment.get_clinic_phone_number }}
        </p>
        <p>
            If you *cannot* make the clinic appointment, please contact the organization to let them know so someone else
            can be scheduled instead.
        </p>
        <p>
            PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have
            questions about your clinic appointment, please contact {{ clinic_name }} at
            {{ appointment.get_clinic_phone_number }}.
        </p>
    {% endwith %}
{% endblock %}
