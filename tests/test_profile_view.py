import json
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from app import models


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


@pytest.mark.django_db
def test_change_donation_status(client, prepare_data):
    user = prepare_data.get("user")
    client.force_login(user)
    donation = prepare_data.get("donation")
    assert donation.is_taken is False
    data = {
        "donationId": f"{donation.pk}",
        "takenStatus": "true",
    }
    response = client.post(
        reverse('app:profile'),
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    new_donation = models.Donation.objects.get(pk=donation.pk)
    assert new_donation.is_taken is True

    # Immediate reverse
    data = {
        "donationId": f"{new_donation.pk}",
        "takenStatus": "false",
    }
    response = client.post(
        reverse('app:profile'),
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    new_donation = models.Donation.objects.get(pk=new_donation.pk)
    assert new_donation.is_taken is False


@pytest.mark.django_db
def test_change_donation_status_not_possible_for_different_user(client, prepare_data, full_user):
    client.force_login(full_user)
    donation = prepare_data.get("donation")
    assert donation.is_taken is False
    data = {
        "donationId": f"{donation.pk}",
        "takenStatus": "true",
    }
    response = client.post(
        reverse('app:profile'),
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 302
    assert response.url == reverse("app:home")
    donation = models.Donation.objects.get(pk=donation.pk)
    assert donation.is_taken is False
