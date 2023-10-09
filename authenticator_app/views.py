from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django_ratelimit.decorators import ratelimit
from authenticator_app.models import User
# from allauth.account.views import SignupView # Delete if it is not working
# from allauth.account.utils import complete_signup 

# Create your views here.


@ratelimit(key='user', rate='5/h', method='POST', block=True) #Rate Limit

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

            # user = complete_signup(request, form.user, "allauth.account.signup")
            # # The above line will create the user account and send an email verification link.
            # return redirect('account_login')  # Redirect to the login page
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form':form})
    # return render(request, 'account/signup.html', {'form': form})

def login(request):
    return render(request, 'login.html')
    
