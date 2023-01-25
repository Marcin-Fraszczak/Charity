from datetime import datetime
import pytest
from app import models


@pytest.mark.django_db
def test_add_category_to_db():
    name = "test_cat"
    models.Category.objects.create(name=name)
    category = models.Category.objects.get(name=name)
    assert str(category) == name


@pytest.mark.django_db
def test_add_institution_to_db():
    name = "test_inst"
    models.Institution.objects.create(
        name=name,
        description="test_desc",
        type=1,
    )
    institution = models.Institution.objects.get(name=name)
    assert str(institution) == name


@pytest.mark.django_db
def test_add_donation_to_db(prepare_data):
    user = prepare_data.get("user")
    institution = prepare_data.get("institution")
    address = "aaa 20"
    pick_up_date = datetime(year=2022, month=10, day=1, hour=10, minute=10)
    models.Donation.objects.create(
        quantity=1,
        institution=institution,
        address=address,
        phone_number="123456789",
        city="Poznan",
        zip_code="12-345",
        pick_up_date=pick_up_date.date(),
        pick_up_time=pick_up_date.time(),
        user=user,
    )
    donation = models.Donation.objects.get(address=address)
    assert str(donation) == f"{address}, {pick_up_date.date()}"
