import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from . import models, forms, functions
from django.utils.translation import gettext_lazy as _
from . import sendgrid


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
        form = forms.DonationForm()
        categories = models.Category.objects.all()
        institutions = models.Institution.objects.all()
        countries = [
            {"country": _("Polska"), "number": "+48"},
            {"country": _("Niemcy"), "number": "+49"},
            {"country": _("Ukraina"), "number": "+380"},
        ]
        return render(request, 'form.html', context={
            "categories": categories,
            "institutions": institutions,
            "form": form,
            "countries": countries,
        })

    def post(self, request):
        data = json.loads(request.body)
        form = forms.DonationForm(data)
        if form.is_valid():
            form = form.cleaned_data
            user = request.user
            phone_number = form.get("phone_number")
            address = form.get("address")
            zip_code = form.get("zip_code")
            city = form.get("city")
            bags = form.get("bags")
            pick_up_date = form.get("pick_up_date")
            pick_up_time = form.get("pick_up_time")
            pick_up_comment = form.get("pick_up_comment")
            input_institution = data.get("institution")
            if input_institution.isdigit():
                institution = get_object_or_404(models.Institution, pk=int(input_institution))
            else:
                institution = None

            input_categories = data.get("categories")
            if input_categories:
                cleaned_input_categories = [int(cat) for cat in input_categories if cat.isdigit()]
                categories = [models.Category.objects.get(pk=pk) for pk in cleaned_input_categories]
            else:
                categories = None

            if (categories and institution and
                    functions.validate_phone_number(phone_number) and
                    functions.validate_zip_code(zip_code) and
                    functions.validate_date_and_time(pick_up_date, pick_up_time)
                    and address and city and bags):
                donation = models.Donation.objects.create(
                    quantity=bags,
                    institution=institution,
                    address=address,
                    phone_number=phone_number,
                    city=city,
                    zip_code=zip_code,
                    pick_up_date=pick_up_date,
                    pick_up_time=pick_up_time,
                    pick_up_comment=pick_up_comment,
                    user=user,
                )
                donation.save()
                donation.categories.set(categories)
                donation.save()

                # Send email
                now = datetime.now()
                subject = "Potwierdzenie przekazania daru"
                content = f"""
                To jest automatyczne potwierdzenie, nie odpowiadaj na nie.
                
                Cześć {user.username}!
                Dnia {now.date()} o godzinie {now.strftime("%H:%M")} zarejestrowaliśmy nową darowiznę przekazaną z Twojego konta.
                Szczegóły poniżej:
                
                Kategorie: {', '.join([cat.name for cat in categories])}
                Organizacja: {institution}
                Liczba worków: {bags}
                Adres odbioru: {', '.join([address, zip_code, city])}
                Termin odbioru: {str(pick_up_date) + str(pick_up_time)}
                Dane kontaktowe: {', '.join([user.first_name, user.last_name, phone_number])}
                
                Dziękujemy!
                """
                to_email = user.email
                sendgrid.send_mail(to_email, subject, content)

                # Old, console version
                # donation_email = EmailMessage(subject, content, to=[to_email])
                # donation_email.send()

                return redirect('app:donation_confirmation')
            else:
                messages.error(request, _("Formularz nie został zapisany. Popraw dane"))
                return redirect('app:home')
        else:
            # print("not valid")
            # print(form.errors)
            messages.error(request, form.errors)
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
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:profile')
        else:
            messages.error(request, _("Niepoprawne dane"))
            return redirect('app:register')


class RegisterView(View):
    def get(self, request):
        form = forms.CustomUserCreationForm()
        return render(request, 'register.html', context={"form": form})

    def post(self, request):

        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            first_name = form.cleaned_data.get("name")
            last_name = form.cleaned_data.get("surname")

            user_exists = get_user_model().objects.filter(email=email)
            if user_exists:
                messages.error(request, _("Taki użytkownik już istnieje"))
                return render(request, 'register.html', context={"form": form})

            if password1 != password2:
                return render(request, 'register.html', context={"form": form})

            user = form.save(commit=False)
            user.set_password(password1)
            user.username = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()

            # Send email
            subject = "Aktywacja konta"
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"http://{current_site}/accounts/activate/{uid}/{token}/"
            content = f"Cześć {user.username}!\n Kliknij w poniższy link, by aktywować konto:\n{activation_link}"
            to_email = email
            sendgrid.send_mail(to_email, subject, content)

            # Old, console version
            # activation = EmailMessage(subject, content, to=[to_email])
            # activation.send()

            messages.success(request, _("Utworzono nowe konto"))
            return render(request, "registration/activation_link_sent.html")

        messages.error(request, _("Błąd podczas zapisywania formularza"))
        return render(request, 'register.html', context={"form": form})


class ActivateView(View):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = get_user_model().objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            # activate user and log in:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, _("Pomyślnie aktywowano konto"))
            return redirect("app:profile")
        messages.error(request, _("Błędny link aktywacyjny"))
        return redirect("app:register")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('app:home')


def json_donation(donation, status):
    donation = {
        "pk": donation.pk,
        "quantity": donation.quantity,
        "categories": [cat.name for cat in donation.categories.all()],
        "institution": donation.institution.name,
        "pick_up_date": donation.pick_up_date,
        "pick_up_time": donation.pick_up_time,
        "is_taken": donation.is_taken,
        "status": status,
    }

    data = {
        "donation": donation,
    }
    return data


class ProfileView(View):
    def get(self, request):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        donations = models.Donation.objects.filter(user=user).order_by("pick_up_date")
        return render(request, "profile.html", context={"user": user, "donations": donations})

    def post(self, request):
        data = json.loads(request.body)
        donation = get_object_or_404(models.Donation, pk=data.get("donationId"))
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)

        if donation.user == user:
            status = data.get("takenStatus")
            if status == 'true':
                donation.is_taken = True
            else:
                donation.is_taken = False
            donation.save()
            return JsonResponse(json_donation(donation, status))
        else:
            messages.error(request, _("Nie masz uprawnień do modyfikacji"))
            return redirect('app:home')


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        User = get_user_model()
        user = get_object_or_404(User, pk=request.user.pk)
        form = forms.CustomUserCreationForm(initial={
            "name": user.first_name,
            "surname": user.last_name,
            "email": user.email,
        })
        return render(request, 'settings.html', context={"form": form})

    def post(self, request):

        form = forms.CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            print("valid")
            user = request.user
            data = form.cleaned_data
            email = data.get("email")
            first_name = data.get("name")
            last_name = data.get("surname")
            password = data.get("password1")

            # check if a new email is already taken
            email_exists = get_user_model().objects.filter(email=email)
            for e_e in email_exists:
                if e_e.pk != user.pk:
                    messages.error(request, _("Inny użytkownik ma już taki adres email"))
                    return redirect('app:settings')
            # check if the password is correct and make changes
            user = get_object_or_404(get_user_model(), pk=user.pk)
            if user.check_password(password):
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = email
                user.save()
                messages.success(request, _("Poprawnie zmieniono dane"))
                return redirect('app:profile')
            else:
                messages.error(request, _("Podano niepoprawne dane"))
                return redirect("app:settings")

        messages.error(request, _("Podano niepoprawne dane"))
        return redirect("app:settings")


class CloseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = forms.CustomUserCreationForm(initial={
            "email": user.email,
        })
        return render(request, "close.html", context={"form": form})

    def post(self, request):
        user = request.user
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password1")
            if user.check_password(password):
                user.is_active = False
                user.save()
                messages.success(request, _("Konto zostało zamknięte."))
                return redirect("app:home")
        messages.error(request, _("Niepoprawne dane"))
        return redirect("app:close")


class CheckEmailView(View):
    def post(self, request):
        email = json.loads(request.body).get("email")

        try:
            validate_email(email)
            valid = True
        except ValidationError:
            valid = False

        if valid:
            exists = get_user_model().objects.filter(email=email)
        else:
            exists = []

        return JsonResponse({"email": email, "valid": valid, "exists": len(exists)})


class ContactView(View):
    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        message = request.POST.get("message")
        origin_site = request.headers.get("referer")
        if name and surname and message:
            if len(name) >= 3 and len(surname) >= 3 and len(message) >= 10:
                name = escape(name)
                surname = escape(surname)
                message = escape(message)

                # Send email
                now = datetime.now()
                admins = get_user_model().objects.filter(is_staff=1)
                subject = "Formularz kontaktowy: nowa wiadomość"
                content = f"""
                                {now.strftime('%Y/%m/%d %H:%M:%s')}
                                Nowa wiadomość od {name} {surname}:
                                
                                {message}
                                """

                to_emails = (admin.email for admin in admins)
                for to_email in to_emails:
                    sendgrid.send_mail(to_email, subject, content)

                # Old, console version
                # message = EmailMessage(subject, content, to=[to_email])
                # message.send()

                messages.success(request, _("Wiadomość wysłano pomyślnie"))
                return redirect(origin_site)

        messages.error(request, _("Wiadomość nie została wysłana. Niepoprawnie wypełniony formularz"))
        return redirect(origin_site)
