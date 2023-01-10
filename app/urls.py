from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add-donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('donation-confirmation/', views.DonationConfirmedView.as_view(), name='donation_confirmation'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/settings/', views.SettingsView.as_view(), name='settings'),
    path('accounts/close/', views.CloseView.as_view(), name='close'),
    path('accounts/changepass/', views.ChangePasswordView.as_view(), name='change_password'),
]
