import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_url_exists_at_correct_location(client):
    response = client.get("/accounts/register/")
    assert response.status_code == 200
    response = client.get(reverse("app:register"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_correct_template_loaded(client):
    response = client.get(reverse("app:register"))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'register.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')


@pytest.mark.django_db
def test_correct_content_loaded(client):
    response = client.get(reverse("app:register"))
    content = response.content.decode('utf-8')
    assert '<h2>Załóż konto</h2>' in content


@pytest.mark.django_db
def test_sign_up_form_and_activation_link(client):
    response = client.post(
        reverse("app:register"), {
            "email": "test@gmail.com",
            "password1": "Testpass123",
            "password2": "Testpass123",
        })
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert str(messages[0]) == "Utworzono nowe konto"

    # Proceed wth activation
    user = get_user_model().objects.get(email="test@gmail.com")
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    response = client.get(
        reverse('app:activate', args=[f"{uid}", f"{token}"]))
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url == reverse('app:profile')
    assert str(messages[0]) == "Pomyślnie aktywowano konto"


@pytest.mark.django_db
def test_user_already_exists(client, full_user):
    response = client.post(
        reverse("app:register"), {
            "email": full_user.email,
            "password1": "Testpass123",
            "password2": "Testpass123",
        })
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert str(messages[0]) == "Taki użytkownik już istnieje"


@pytest.mark.django_db
def test_two_passwords_not_the_same(client):
    response = client.post(
        reverse("app:register"), {
            "email": "test@gmail.com",
            "password1": "Testpass123",
            "password2": "Testpass12344",
        })
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert str(messages[0]) == "Błąd podczas zapisywania formularza"
