{% extends 'mail_templated/base.tpl' %}

{% block subject %}
    Please complete your legal clinic waiver
{% endblock subject %}

{% block body %}
    {% with clinic_name=appointment.get_clinic_name %}
    Thanks for contacting {{ clinic_name }}. Before we can look for an attorney to assist you with an advisory consultation,
    you need to first complete the waiver which can be found [NEED THE WAIVER FILES OR URLS].

    Please fill out the waiver and return it to {{ clinic_name }}. Once you've signed and returned the waiver
    we can begin to look for an attorney to assist you. Unfortunately, we cannot guarantee that we can find
    an attorney, as all clinic attorneys assist people on a volunteer basis, and the demand for pro bono
    attorneys is greater than the supply.

    PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have questions
    about your clinic appointment, please contact {{ clinic_name }} at {{ appointment.get_clinic_phone_number }}.
    {% endwith %}
{% endblock body %}

{% block html %}
    {% with clinic_name=appointment.get_clinic_name %}
        <p>
            Thanks for contacting {{ clinic_name }}. Before we can look for an attorney to assist you with an advisory
            consultation, you need to first complete the waiver which can be found [NEED THE WAIVER FILES OR URLS].
        </p>

        <p>
            Please fill out the waiver and return it to {{ clinic_name }}. Once you've signed and returned the waiver
            we can begin to look for an attorney to assist you. Unfortunately, we cannot guarantee that we can find
            an attorney, as all clinic attorneys assist people on a volunteer basis, and the demand for pro bono
            attorneys is greater than the supply.
        </p>

        <p>
            PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have
            questions about your clinic appointment, please contact {{ clinic_name }} at
            {{ appointment.get_clinic_phone_number }}.
        </p>
    {% endwith %}
{% endblock html %}
