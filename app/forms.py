from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models

pass_help_text = """
<br>- Przynajmniej 8 znaków 
<br>- Musi zawierać przynajmniej jedną wielką literę 
<br>- Nie może być zbyt pospolite lub podobne do pozostałych danych
<br>- Nie może być w całości numeryczne
"""


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
    bags = forms.IntegerField(widget=forms.widgets.NumberInput)
    pick_up_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    pick_up_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    pick_up_comment = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = models.Donation
        fields = [
            # "quantity",
            # "categories",
            # "institution",
            "address",
            "phone_number",
            "city",
            "zip_code",
            # "pick_up_date",
            # "pick_up_time",
            # "pick_up_comment",
        ]

