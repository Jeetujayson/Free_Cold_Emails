from django.urls import path
from . import views
from authenticator_app import views as authenticator_views

urlpatterns = [
    path ("", views.index, name="index"),
    path('login/', authenticator_views.login, name='login'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service')

]