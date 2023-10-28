from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import CustomSignupForm

# Create your views here.

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    
    ## added to make user inactive by default
    # def form_valid(self, form):
    #     # Call the parent form_valid method to save the user
    #     response = super().form_valid(form)
    #     # Check if the user has verified their email
    #     if self.user.emailaddress_set.filter(verified=True).exists():
    #         self.user.is_active = True
    #         self.user.save()
    #     return response

def index(request):
    return render(request, "index.html")

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

def email_verification(request):
    return render(request, 'buy_me_caffeine.html')
