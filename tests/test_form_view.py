import json
from datetime import datetime

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from app import models


@pytest.mark.django_db
def test_url_exists_at_correct_location(client, user):
    client.force_login(user)
    response = client.get("/add-donation/")
    assert response.status_code == 200
    response = client.get(reverse("app:add_donation"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_correct_template_loaded(client, user):
    client.force_login(user)
    response = client.get(reverse("app:add_donation"))
    assertTemplateUsed(response, '_base.html')
    assertTemplateUsed(response, 'form.html')
    assertTemplateUsed(response, 'partials/_menu2.html')
    assertTemplateUsed(response, 'partials/_footer.html')

