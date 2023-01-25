import json
from datetime import datetime

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from app import models


# @pytest.mark.django_db
# def test_add_donation_form(client, prepare_data):
#     user = prepare_data.get("user")
#     client.force_login(user)
#     address = "bbb 20"
#     data = {
#         "categories": prepare_data.get("category").pk,
#         "quantity": 4,
#         "institution": prepare_data.get("institution").pk,
#         "address": address,
#         "phone_number": "+48123456789",
#         "city": "Poznan",
#         "zip_code": "12-345",
#         "pick_up_date": "2022-10-10",
#         "pick_up_time": "10:10",
#     }
#     response = client.post(
#         reverse('app:add_donation'),
#         data=json.dumps(data, separators=(',', ':')),
#         headers={"Content-Type": "application/json"},
#     )
#
#     print(response.status_code)
