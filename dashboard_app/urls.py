from django.urls import path
from . import views
from .views import save_campaign


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/leads/', views.leads, name='leads'),
    path('dashboard/campaigns/', views.campaigns, name='campaigns'),
    path('save_campaign/<int:selected_campaign_id>/', views.save_campaign, name='save_campaign'),

    path('dashboard/schedule/', views.schedule, name='schedule'),


]
