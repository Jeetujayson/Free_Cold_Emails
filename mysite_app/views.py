from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    # Your login view logic here, if needed
    return render(request, 'authenticator_app/login.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

