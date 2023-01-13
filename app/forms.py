from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models, functions


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Imię"}))
    surname = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Nazwisko"}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}))

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('name', 'surname', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['surname'].required = False


class DonationForm(forms.ModelForm):
    bags = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"min": 1, "step": 1}))
    address = forms.CharField(min_length=3)
    phone_number = forms.CharField(min_length=9)
    city = forms.CharField(min_length=3)
    zip_code = forms.CharField(min_length=5)
    pick_up_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', "min": functions.get_tomorrow()}))
    pick_up_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={
        "type": "time", "min": "09:00:00", "max": "20:00:00"}))
    pick_up_comment = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 5}))

    class Meta:
        model = models.Donation
        fields = [
            # "quantity",
            # "categories",
            # "institution",
            "address",
            # "phone_number",
            # "city",
            # "zip_code",
            # "pick_up_date",
            # "pick_up_time",
            # "pick_up_comment",
        ]


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
