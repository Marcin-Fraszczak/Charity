from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('add-donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('donation-confirmation/', views.DonationConfirmedView.as_view(), name='donation_confirmation'),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accountc/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/activate/<str:uid>/<str:token>/', views.ActivateView.as_view(), name='activate'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/settings/', views.SettingsView.as_view(), name='settings'),
    path('accounts/close/', views.CloseView.as_view(), name='close'),
    path('accounts/email/check/', views.CheckEmailView.as_view(), name='check_email'),
    path('accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('accounts/reset/<str:uid>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
