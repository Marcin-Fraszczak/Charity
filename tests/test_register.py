import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
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
def test_sign_up_form(client):
    response = client.post(
        reverse("app:register"), {
            "email": "test@gmail.com",
            "password1": "Testpass123",
            "password2": "Testpass123",
        })
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert str(messages[0]) == "Utworzono nowe konto"

