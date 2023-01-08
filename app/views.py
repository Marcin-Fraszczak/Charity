from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import models, forms, functions


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
        form = forms.DonationForm
        categories = models.Category.objects.all()
        institutions = models.Institution.objects.all()
        return render(request, 'form.html', context={
            "categories": categories,
            "institutions": institutions,
            "form": form,
        })

    def post(self, request):
        print(request.POST)
        form = forms.DonationForm(request.POST)
        if form.is_valid():
            print("valid")
            data = form.cleaned_data
            print(data)

            phone_number = data.get("phone_number")
            zip_code = data.get("zip_code")
            address = data.get("address")
            city = data.get("city")
            bags = data.get("bags")
            pick_up_date = data.get("pick_up_date")
            pick_up_time = data.get("pick_up_time")
            pick_up_comment = data.get("pick_up_comment")

            input_categories = request.POST.get("categories")
            # print(input_categories)
            cleaned_input_categories = [int(cat) for cat in input_categories if cat.isdigit()]
            # print(cleaned_input_categories)
            categories = [models.Category.objects.get(pk=pk) for pk in cleaned_input_categories]

            input_institution = request.POST.get("organization")
            if input_institution.isdigit():
                institution = get_object_or_404(models.Institution, pk=int(input_institution))
            else:
                institution = None

            # print("valid", categories)
            # print("valid", institution)
            # print("datetime", functions.validate_date_and_time(pick_up_date, pick_up_time))
            # print("zip_code", functions.validate_zip_code(zip_code))
            # print("phone_number", functions.validate_phone_number(phone_number))


            if (categories and institution and
                    functions.validate_phone_number(phone_number) and
                    functions.validate_zip_code(zip_code) and
                    functions.validate_date_and_time(pick_up_date, pick_up_time)
                    and address and city and bags):
                print("form validated")
            else:
                print("form not validated")

            return redirect('app:donation_confirmation')
        else:
            print("not valid")
            print(form.errors)
            messages.error(request, "Niepoprawnie wypełniony formularz")
            return redirect('app:add_donation')



class DonationConfirmedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email.split("@")[0], password=password)
        if user is not None:
            login(request, user)
            return redirect('app:home')
        else:
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
                messages.error(request, "Taki użytkownik już istnieje")
                return render(request, 'register.html', context={"form": form})

            if password1 != password2:
                return render(request, 'register.html', context={"form": form})

            user = form.save(commit=False)
            user.set_password(password1)
            user.username = email.split("@")[0]
            user.save()
            messages.success(request, "Utworzono nowe konto")
            return redirect('app:login')

        messages.error(request, "Error saving form")
        return render(request, 'register.html', context={"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('app:home')
