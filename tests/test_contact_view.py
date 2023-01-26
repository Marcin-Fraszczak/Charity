import pytest
from django.contrib.messages import get_messages
from django.urls import reverse


@pytest.mark.django_db
def test_send_message_successful(client, full_user):
    full_user.is_staff = 1
    data = {
        "name": "Alfred",
        "surname": "Thompson",
        "message": "asaksjsakjskajasskas aaa"
    }
    response = client.post(
        reverse('app:contact'),
        data,
    )
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url == reverse("app:home")
    assert str(messages[0]) == "Wiadomość wysłano pomyślnie"



@pytest.mark.django_db
def test_send_message_empty_form(client, full_user):
    full_user.is_staff = 1
    data = {
        "name": "",
        "surname": "",
        "message": ""
    }
    response = client.post(
        reverse('app:contact'),
        data,
    )
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url == reverse("app:home")
    assert str(messages[0]) == "Wiadomość nie została wysłana. Niepoprawnie wypełniony formularz"
