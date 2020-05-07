{% extends 'mail_templated/base.tpl' %}

{% block subject %}
    Please complete your legal clinic waiver
{% endblock subject %}

{% block body %}
    {% with clinic_name=appointment.get_clinic_name %}
        Thanks returning your signed waiver to {{ clinic_name }}. We'll now begin looking for an attorney to assist
        you with an advisory consultation, though unfortunately we cannot guarantee that we will find on, as the demand
        for pro bono attorneys is greater than the supply.

        If we find an attorney who can assist you, we'll email you with the date, time, and location of the legal clinic.

        PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have questions
        about your clinic appointment, please contact {{ clinic_name }} at {{ appointment.get_clinic_phone_number }}.
    {% endwith %}
{% endblock body %}

{% block html %}
    {% with clinic_name=appointment.get_clinic_name %}
        <p>
            Thanks returning your signed waiver to {{ clinic_name }}. We'll now begin looking for an attorney to assist
            you with an advisory consultation, though unfortunately we cannot guarantee that we will find on, as the
            demand for pro bono attorneys is greater than the supply.
        </p>

        <p>
            If we find an attorney who can assist you, we'll email you with the date, time, and location of the legal
            clinic.
        </p>

        <p>
            PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have
            questions about your clinic appointment, please contact {{ clinic_name }} at
            {{ appointment.get_clinic_phone_number }}.
        </p>
    {% endwith %}
{% endblock html %}
