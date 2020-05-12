{% extends 'mail_templated/base.tpl' %}

{% block subject %}
    Please complete your legal clinic waiver
{% endblock subject %}

{% comment %}
{% block body %}
    {% with clinic_name=appointment.organization clinic_abbreviation=appointment.organization.abbreviation %}
    Thanks for contacting {{ clinic_name }} ("{{ clinic_abbreviation }}"). Before we can look for an attorney to assist you with an advisory consultation,
    you need to first complete the waiver which can be found [NEED THE WAIVER FILES OR URLS].

    Please fill out the waiver and return it to {{ clinic_abbreviation }}. Once you've signed and returned the waiver
    we can begin to look for an attorney to assist you. Unfortunately, we cannot guarantee that we can find
    an attorney, as all clinic attorneys assist people on a volunteer basis, and the demand for pro bono
    attorneys is greater than the supply.

    PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have questions
    about your clinic appointment, please contact {{ clinic_name }} at {{ appointment.get_clinic_phone_number }}.
    {% endwith %}
{% endblock body %}
{% endcomment %}

{% block html %}
    {% with clinic_name=appointment.get_clinic_name %}
        <p>
            Thanks for contacting {{ clinic_name }} ("{{ clinic_abbreviation }}"). Before we can look for an attorney to assist you with an advisory
            consultation, you need to first complete the waiver which can be found [NEED THE WAIVER FILES OR URLS].
        </p>

        <p>
            Please fill out the waiver and return it to {{ clinic_abbreviation }}. Once you've signed and returned the
            waiver we can begin to look for an attorney to assist you. Unfortunately, we cannot guarantee that we can
            find an attorney, as all clinic attorneys assist people on a volunteer basis, and the demand for pro bono
            attorneys is greater than the supply.
        </p>
        <p>
            Note: you have the option of uploading your completed waiver. To do that, simply complete the waiver, and
            scan or take a clear photo of it, and then upload the PDF or photo image by
            <a href="{% url 'appointments:appointment_waiver_upload' token=token %}">clicking here</a>

        </p>

        <p>
            PLEASE NOTE: THIS EMAIL ACCOUNT IS UNATTENDED. This means nobody checks for unread messages. If you have
            questions about your clinic appointment, please contact {{ clinic_name }} at
            {{ appointment.get_clinic_phone_number }}.
        </p>
    {% endwith %}
{% endblock html %}
