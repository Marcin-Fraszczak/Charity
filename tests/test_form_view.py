import pytest
import json
from django.urls import reverse
from django.contrib.messages import get_messages
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


@pytest.mark.django_db
def test_add_donation_form(client, prepare_data):
    user = prepare_data.get("user")
    client.force_login(user)
    address = "bbb 20"
    data = {
        "categories": f'{prepare_data.get("category").pk}',
        "bags": "4",
        "institution": f'{prepare_data.get("institution").pk}',
        "address": address,
        "phone_number": "+48123456781",
        "city": "Poznan",
        "zip_code": "12-345",
        "pick_up_date": "2040-10-10",
        "pick_up_time": "10:10",
    }
    response = client.post(
        reverse('app:add_donation'),
        data=json.dumps(data),
        content_type="application/json",
    )
    donation = models.Donation.objects.get(phone_number="+48123456781")
    assert response.status_code == 302
    assert response.url == reverse('app:donation_confirmation')
    assert donation.city == "Poznan"

    # Immediately check confirmation page
    response = client.get(response.url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'form-confirmation.html')


@pytest.mark.django_db
def test_add_donation_form_with_wrong_data(client, prepare_data):
    user = prepare_data.get("user")
    client.force_login(user)
    zip_code = "123456"
    data = {
        "categories": f'a, 100',
        "bags": "3",
        "institution": f'a',
        "address": "bbb 10",
        "phone_number": "+48123456789",
        "city": "Poznan",
        "zip_code": zip_code,
        "pick_up_date": "2010-10-10",
        "pick_up_time": "21:10",
    }
    response = client.post(
        reverse('app:add_donation'),
        data=json.dumps(data),
        content_type="application/json",
    )
    messages = list(get_messages(response.wsgi_request))
    donation = models.Donation.objects.filter(zip_code=zip_code)
    assert len(donation) == 0
    assert response.status_code == 302
    assert response.url == reverse('app:home')
    assert len(messages) > 0
