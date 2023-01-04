import json

from django.core.paginator import Paginator
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

        foundations = models.Institution.objects.filter(type=1).order_by("name")
        organizations = models.Institution.objects.filter(type=2).order_by("name")
        collections = models.Institution.objects.filter(type=3).order_by("name")
        results_per_page = 5

        paginated_foundations = Paginator(foundations, results_per_page)
        pf_dict = {page: paginated_foundations.page(page) for page in paginated_foundations.page_range}
        pf_page_range = paginated_foundations.get_elided_page_range(
            paginated_foundations.num_pages, on_each_side=2, on_ends=2)

        paginated_organizations = Paginator(organizations, results_per_page)
        po_dict = {page: paginated_organizations.page(page) for page in paginated_organizations.page_range}
        paginated_collections = Paginator(collections, results_per_page)
        pc_dict = {page: paginated_collections.page(page) for page in paginated_collections.page_range}


        context.update({
            "pf_dict": pf_dict,
            "pf_page_range": pf_page_range,
            "po_dict": po_dict,
            "pc_dict": pc_dict,
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
