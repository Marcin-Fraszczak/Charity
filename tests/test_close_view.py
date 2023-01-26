import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    client.force_login(user)
    response = client.get("/accounts/close/")
    assert response.status_code == 200
    response = client.get(reverse("app:close"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_correct_template_loaded(client, user):
    client.force_login(user)
    response = client.get(reverse("app:close"))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'close.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')


@pytest.mark.django_db
def test_correct_content_loaded(client, full_user):
    client.force_login(full_user)
    response = client.get(reverse("app:close"))
    content = response.content.decode('utf-8')
    assert 'Zamknij konto' in content


@pytest.mark.django_db
def test_close_account_successful(client, full_user):
    client.force_login(full_user)
    full_user.is_active = True
    data = {
        "password1": "Testpass123",
        "password2": "Testpass123",
        "email": f"{full_user.email}",
    }
    response = client.post(
        reverse('app:close'), data)
    assert response.status_code == 302
    assert response.url == reverse("app:home")
    user = get_user_model().objects.get(email=full_user.email)
    assert user.is_active is False


@pytest.mark.django_db
def test_close_account_with_wrong_input(client, full_user):
    client.force_login(full_user)
    full_user.is_active = True
    data = {
        "password1": "Testpass123aa",
        "password2": "Testpass123aa",
        "email": f"{full_user.email}",
    }
    response = client.post(
        reverse('app:close'), data)
    assert response.status_code == 302
    assert response.url == reverse("app:close")
    user = get_user_model().objects.get(email=full_user.email)
    assert user.is_active is True
