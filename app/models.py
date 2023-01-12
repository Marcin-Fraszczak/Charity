from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _



TYPES = (
    (1, _("fundacja")),
    (2, _("organizacja pozarządowa")),
    (3, _("zbiórka lokalna")),
)


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, blank=True, null=True)
    type = models.IntegerField(choices=TYPES, default=1)
    categories = models.ManyToManyField('Category', related_name='institution')

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category', related_name='donation')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=13)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, default=None)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address}, {self.pick_up_date}"


# class Message(models.Model):
#     name = models.CharField(max_length=60, validators=[MinLengthValidator(3)])
#     surname = models.CharField(max_length=60, validators=[MinLengthValidator(3)])
#     email = models.EmailField()
#     message = models.TextField(validators=[MinLengthValidator(10)])
#     sent_when = models.DateTimeField(auto_now=True)
#