import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    client.force_login(user)
    response = client.get("/accounts/settings/")
    assert response.status_code == 200
    response = client.get(reverse("app:settings"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_correct_template_loaded(client, user):
    client.force_login(user)
    response = client.get(reverse("app:settings"))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'settings.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')


@pytest.mark.django_db
def test_correct_content_loaded(client, full_user):
    client.force_login(full_user)
    response = client.get(reverse("app:settings"))
    content = response.content.decode('utf-8')
    assert f'Zmień dane' in content


@pytest.mark.django_db
def test_change_personal_data_success(client, full_user):
    client.force_login(full_user)
    response = client.post(
        reverse("app:settings"), {
            "name": "aaaa",
            "surname": "bbbb",
            "password1": "Testpass123",
            "password2": "Testpass123",
            "email": "test11@gmail.com",
        })
    messages = list(get_messages(response.wsgi_request))
    user = get_user_model().objects.get(email="test11@gmail.com")
    assert response.status_code == 302
    assert user
    assert str(messages[0]) == "Poprawnie zmieniono dane"



@pytest.mark.django_db
def test_change_personal_data_invalid_password(client, full_user):
    client.force_login(full_user)
    response = client.post(
        reverse("app:settings"), {
            "name": "aaaa",
            "surname": "bbbb",
            "password1": "Testpass1234",
            "password2": "Testpass1234",
            "email": "test11@gmail.com",
        })
    messages = list(get_messages(response.wsgi_request))
    user = get_user_model().objects.filter(email="test11@gmail.com")
    assert response.status_code == 302
    assert len(user) == 0
    assert str(messages[0]) == "Podano niepoprawne dane"


@pytest.mark.django_db
def test_change_email_already_exists(client, full_user, user):
    client.force_login(user)
    response = client.post(
        reverse("app:settings"), {
            "name": "aaaa",
            "surname": "bbbb",
            "password1": "Testpass1234",
            "password2": "Testpass1234",
            "email": f"{full_user.email}",
        })
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url == reverse('app:settings')
    assert str(messages[0]) == "Inny użytkownik ma już taki adres email"



@pytest.mark.django_db
def test_change_personal_data_with_wrong_input(client, full_user):
    client.force_login(full_user)
    response = client.post(
        reverse("app:settings"), {
            "name": "aaaa",
            "surname": "bbbb",
            "password1": "Testpass1234",
            "password2": "Testpass1234",
            "email": f"aaaaa",
        })
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url == reverse('app:settings')
    assert str(messages[0]) == "Podano niepoprawne dane"
