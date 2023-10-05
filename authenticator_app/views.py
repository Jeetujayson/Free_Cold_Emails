from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django_ratelimit.decorators import ratelimit
from authenticator_app.models import User



# Create your views here.


@ratelimit(key='user', rate='5/h', method='POST', block=True) #Rate Limit

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form':form})

def login(request):
    return render(request, 'login.html')


# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = RegistrationForm()

    # return render(request, 'register.html', {'form':form})