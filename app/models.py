from django.db import models
from django.contrib.auth.models import User

TYPES = (
    (1, "fundacja"),
    (2, "organizacja pozarządowa"),
    (3, "zbiórka lokalna"),
)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    type = models.IntegerField(choices=TYPES, default=1)
    categories = models.ManyToManyField('Category', related_name='institution')


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category', related_name='donation')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
