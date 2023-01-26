import json
import pytest
from django.http import JsonResponse
from django.urls import reverse


@pytest.mark.django_db
def test_check_email_successful(client, full_user):
    client.force_login(full_user)
    data = {
        "email": f"{full_user.email}",
    }
    response = client.post(
        reverse('app:check_email'),
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert response.json().get("exists") != 0



@pytest.mark.django_db
def test_check_email_not_exists(client, full_user):
    client.force_login(full_user)
    data = {
        "email": f"aaa@aaa.com",
    }
    response = client.post(
        reverse('app:check_email'),
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert response.json().get("exists") == 0


@pytest.mark.django_db
def test_check_email_wrong_format(client, full_user):
    client.force_login(full_user)
    data = {
        "email": f"aaaaaa.com",
    }
    response = client.post(
        reverse('app:check_email'),
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert response.json().get("exists") == 0
