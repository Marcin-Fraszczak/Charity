import pytest
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


