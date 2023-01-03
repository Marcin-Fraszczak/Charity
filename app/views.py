from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from . import models


class HomeView(View):
    def get(self, request):
        all_donations = models.Donation.objects.all()
        total_bags = sum([int(donation.quantity) for donation in all_donations])
        total_institutions = len(set([donation.institution for donation in all_donations]))
        context = {"total_bags": total_bags, "total_institutions": total_institutions}

        if "fetch" in request.GET:
            data = context
            return JsonResponse(data)

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
