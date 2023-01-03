import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from . import models


class HomeView(View):
    def get(self, request):
        all_donations = models.Donation.objects.all()
        total_bags = sum([int(donation.quantity) for donation in all_donations])
        total_institutions = len(set([donation.institution for donation in all_donations]))

        context = {
            "total_bags": total_bags,
            "total_institutions": total_institutions,
        }
        if "fetch_stats" in request.GET:
            data = context
            return JsonResponse(data)

        foundations = models.Institution.objects.filter(type=1)
        organizations = models.Institution.objects.filter(type=2)
        collections = models.Institution.objects.filter(type=3)
        results_per_page = 5

        context.update({
            "foundations": foundations,
            "foundations_pages": [i for i in range(1, -(-len(foundations) // results_per_page) + 1)],
            "organizations": organizations,
            "organizations_pages": [i for i in range(1, -(-len(organizations) // results_per_page) + 1)],
            "collections": collections,
            "collections_pages": [i for i in range(1, -(-len(collections) // results_per_page) + 1)],
            "results_per_page": results_per_page,
        })

        return render(request, 'index.html', context)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
