import pytest
from django.contrib.auth import get_user_model
from django.test import Client


name = 'testuser'


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = get_user_model()(username=name)
    user.save()
    return user

