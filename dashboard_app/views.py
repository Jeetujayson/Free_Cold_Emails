from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def db_view(request):
    return render(request, 'db.html')