import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    client.force_login(user)
    response = client.get("/accounts/profile/")
    assert response.status_code == 200
    response = client.get(reverse("app:profile"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_correct_template_loaded(client, user):
    client.force_login(user)
    response = client.get(reverse("app:profile"))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'profile.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')


@pytest.mark.django_db
def test_correct_content_loaded(client, full_user):
    client.force_login(full_user)
    response = client.get(reverse("app:profile"))
    content = response.content.decode('utf-8')
    assert f'Witaj {full_user.email}' in content


