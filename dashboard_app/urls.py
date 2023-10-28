from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/leads/', views.leads, name='leads'),
    path('dashboard/message_draft/', views.message_draft, name='message_draft'),
    path('dashboard/schedule/', views.schedule, name='schedule'),


]
