from django.urls import path
from . import views

# from allauth.account.views import LoginView  # Import the LoginView from Allauth
# from allauth.account.views import SignupView, LoginView

from .views import CustomSignupView



urlpatterns = [
    path ("", views.index, name="index"),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('email_verification/', views.email_verification, name='email_verification'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    
    

    # path('login/', authenticator_views.login, name='login'),
    # path('signup/', SignupView.as_view(), name='signup'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('accounts/login/', LoginView.as_view(), name='account_login'),
]