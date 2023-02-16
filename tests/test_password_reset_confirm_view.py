"""
Only for Sendgrid
"""


# import pytest
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.messages import get_messages
# from django.urls import reverse
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from pytest_django.asserts import assertTemplateUsed
#
#
# @pytest.mark.django_db
# def test_password_reset_get_success(client, user):
#     client.force_login(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#     response = client.get(
#         reverse('app:password_reset_confirm', args=[f"{uid}", f"{token}"]))
#     assert response.status_code == 200
#     assertTemplateUsed(response, '_base.html')
#     assertTemplateUsed(response, 'registration/password_reset_confirm.html')
#     assertTemplateUsed(response, 'partials/_menu2.html')
#     assertTemplateUsed(response, 'partials/_footer.html')
#
#
# @pytest.mark.django_db
# def test_password_reset_get_invalid_link(client, user):
#     client.force_login(user)
#     uid = "aaa"
#     token = "bbb"
#     response = client.get(
#         reverse('app:password_reset_confirm', args=[f"{uid}", f"{token}"]))
#     messages = list(get_messages(response.wsgi_request))
#     assert response.status_code == 302
#     assert response.url == reverse("app:login")
#     assert str(messages[0]) == "Błędny link aktywacyjny"
