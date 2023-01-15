import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_url_exists_at_correct_location(client):
    response = client.get("/")
    assert response.status_code == 200
    response = client.get(reverse("app:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_correct_template_loaded(client):
    response = client.get(reverse("app:home"))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'index.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')
