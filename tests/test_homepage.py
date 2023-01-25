import json

import pytest
from django.http import JsonResponse
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


@pytest.mark.django_db
def test_correct_content_loaded(client):
    response = client.get(reverse("app:home"))
    content = response.content.decode('utf-8')
    assert "Zacznij pomagać" in content
    assert "Wystarczą 4 proste kroki" in content
    assert "O nas" in content
    assert "Komu pomagamy?" in content


@pytest.mark.django_db
def test_correct_data_fetched_from_db(client, prepare_data):
    response = client.get(reverse("app:home"))
    content = response.content.decode('utf-8')
    assert f'<em class="total_bags">{prepare_data["bags"]}</em>' in content
    assert f'<em class="total_institutions">1</em>' in content


@pytest.mark.django_db
def test_js_fetch_working(client):
    response = client.get(reverse('app:home'), {"fetch_stats": 1})
    assert isinstance(response, JsonResponse)


