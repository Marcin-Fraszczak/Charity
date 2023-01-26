import pytest
from django.contrib.messages import get_messages
from django.contrib import auth
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_url_exists_at_correct_location(client):
    response = client.get('/accounts/login/')
    assert response.status_code == 200
    response = client.get(reverse('app:login'))
    assert response.status_code == 200


def test_correct_template_loaded(client):
    response = client.get(reverse('app:login'))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'login.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')


@pytest.mark.django_db
def test_login_with_correct_data_then_logout(client, full_user):
    response = client.post(
        reverse('app:login'),
        {"email": full_user.email,
         "password": "Testpass123"
         })
    assert response.status_code == 302
    assert response.url == reverse('app:profile')
    user = auth.get_user(client)
    assert user.is_authenticated

    # Immediate logout
    response = client.get(reverse('app:logout'))
    assert response.status_code == 302
    assert response.url == reverse('app:home')
    user = auth.get_user(client)
    assert not user.is_authenticated


@pytest.mark.django_db
def test_login_with_incorrect_data(client, full_user):
    response = client.post(
        reverse('app:login'),
        {"email": full_user.email+"aa",
         "password": "Testpass123"+"aa",
         })
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url == reverse('app:register')
    assert str(messages[0]) == "Niepoprawne dane"
