from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . import models
from . import forms


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


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = models.Category.objects.all()
        return render(request, 'form.html', context={"categories": categories})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            print("jest zalogowany")
            return redirect('app:home')
        else:
            print("nie ma takiego numeru")
            messages.error(request, "Invalid data")
            return redirect('app:register')


class RegisterView(View):
    def get(self, request):
        form = forms.CustomUserCreationForm
        return render(request, 'register.html', context={"form": form})

    def post(self, request):

        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")

            user_exists = get_user_model().objects.filter(email=email)
            if user_exists:
                messages.error(request, "User already exists")
                return render(request, 'register.html', context={"form": form})

            if password1 != password2:
                return render(request, 'register.html', context={"form": form})

            user = form.save(commit=False)
            user.set_password(password1)
            user.username = email
            user.save()
            messages.success(request, "User successfully created")
            return redirect('app:login')

        messages.error(request, "Error saving form")
        return render(request, 'register.html', context={"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('app:home')
