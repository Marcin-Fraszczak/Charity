import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from app.models import Category, Institution, Donation

name = 'testuser'


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def full_user():
    user = get_user_model()(
        email="test@gmail.com",
        username="test@gmail.com",
        password="Testpass123"
    )
    user.save()
    user.set_password('Testpass123')
    user.save()

    return user


@pytest.fixture
def user():
    user = get_user_model()(
        username=name
    )
    user.save()
    user.set_password('Testpass123')
    user.save()
    return user


@pytest.fixture
def prepare_data(user):
    bags = 5
    category = Category.objects.create(name="zabawki")
    institution = Institution.objects.create(
        name="testowa instytucja",
        description="opis testowy",
        type=1,
        )
    institution.categories.add(category)
    institution.save()
    donation = Donation.objects.create(
        quantity=bags,
        institution=institution,
        address="Staszica 40",
        phone_number="+48123456789",
        zip_code="23-230",
        pick_up_time="15:00",
        pick_up_date="2030-01-10",
        user=user,
        is_taken=False,
    )
    donation.categories.add(category)
    donation.save()
    return {
        "user": user,
        "category": category,
        "institution": institution,
        "donation": donation,
        "bags": bags,
    }
