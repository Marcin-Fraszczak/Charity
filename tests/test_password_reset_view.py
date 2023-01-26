import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    client.force_login(user)
    response = client.get("/accounts/password_reset/")
    assert response.status_code == 200
    response = client.get(reverse("app:password_reset"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_correct_template_loaded(client, user):
    client.force_login(user)
    response = client.get(reverse("app:password_reset"))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'registration/password_reset_form.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')


@pytest.mark.django_db
def test_password_change_form_success(client, full_user):
    client.force_login(full_user)
    data = {
        "email": f"{full_user.email}",
    }
    response = client.post(
        reverse('app:password_reset'), data)
    assert response.status_code == 302
    assert response.url == reverse('password_reset_done')


@pytest.mark.django_db
def test_password_change_form_wrong_data(client, full_user):
    client.force_login(full_user)
    data = {
        "email": f"aaaa",
    }
    response = client.post(
        reverse('app:password_reset'), data)
    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert response.url == reverse('app:password_reset')
    assert str(messages[0]) == "Nie ma takiego użytkownika w bazie danych"
