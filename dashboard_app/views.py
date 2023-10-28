from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.db.utils import IntegrityError  # Import IntegrityError
from .forms import SmtpForm
from .models import SmtpModel

from django.http import JsonResponse  # Import JsonResponse for AJAX responses
import smtplib
from django.contrib import messages

from .smtp_verification import validate_smtp_data

from django.shortcuts import render, redirect
from .forms import SmtpForm
from .models import SmtpModel
from .smtp_verification import validate_smtp_data
from django.core.exceptions import ValidationError

from mysite_app.models import AccountLimit  # Import the AccountLimits model

@login_required
def dashboard(request):
    error_message = None
    show_overlay = False  # Add a flag to control the overlay

    if request.method == 'POST': #If user submits a form
        show_overlay = True  # Set the flag to show the overlay
        form = SmtpForm(request.POST) # collect input data from form fields
        
        # For Delete Button
        if 'delete_smtp' in request.POST:
            
            delete_smtp = request.POST['delete_smtp']
            try:
                smtp_data_to_delete = SmtpModel.objects.get(id=delete_smtp, user=request.user)
                smtp_data_to_delete.delete()
                linked_emails = SmtpModel.objects.filter(user=request.user)
                return render(request, 'db.html', {'linked_emails': linked_emails,})
            except SmtpModel.DoesNotExist:
                error_message = "The requested email doesn't exist or doesn't belong to your account."
                # You can customize this error message as needed
        else:
            print("A")
            user = request.user
            account_limit = AccountLimit.objects.get(user=user)
            print("B")
            if account_limit.smtp_limit > SmtpModel.objects.filter(user=user).count():
                print("C")
                if form.is_valid():
                    print("D")
                    user = request.user
                    smtp_data = form.save(commit=False) # creates an instance of the form
                    smtp_data.user = request.user
                    print("E")
                    try:
                        print("F")
                        smtp_data.full_clean()  # This will call the form's clean method
                        
                        print("saving to DB")
                        smtp_data.save()
                        print("Saved to DB")
                    except ValidationError as e:
                        print(e)
                        print("SDASDSDASDASDASD")
                        error_message = str(e)
                        print(error_message)

                        

                            
                else:
                    print("form not valid")
                    print(form.errors)
                    error_message = form.non_field_errors()
            else:
                print("G")
                error_message = "You have reached the maximum allowed SMTP configurations."
                linked_emails = SmtpModel.objects.filter(user=request.user)
                return render(request, 'db.html', {'linked_emails': linked_emails, 'error_message': error_message, 'show_overlay': show_overlay,})
        print("H")
        linked_emails = SmtpModel.objects.filter(user=request.user)
        print("I")
    else:
        print("J")
        form = SmtpForm() # to display an empty form if it is GET request usually on first page load
        linked_emails = SmtpModel.objects.filter(user=request.user)
    show_overlay = False  # Set the flag to show the overlay
    return render(request, 'db.html', {'form': form, 'linked_emails': linked_emails, 'error_message': error_message, 'show_overlay': show_overlay,})

# @login_required
# def dashboard(request):
#     if request.method == 'POST':
#         form = SmtpForm(request.POST)

#         if 'delete_smtp' in request.POST:
#             delete_smtp = request.POST['delete_smtp']
#             # Perform the deletion
#             try:
#                 smtp_data_to_delete = SmtpModel.objects.get(id=delete_smtp, user=request.user)
#                 smtp_data_to_delete.delete()
#             except SmtpModel.DoesNotExist:
#                 # Handle the case where the requested email doesn't exist or doesn't belong to the user
#                 pass  # You can add appropriate error handling here

#             # Redirect back to the same page to refresh the table
#             return redirect('dashboard')
    
#     # Handle the form for adding new SMTP data
#     form = SmtpForm()
#     linked_emails = SmtpModel.objects.filter(user=request.user)

#     return render(request, 'db.html', {'form': form, 'linked_emails': linked_emails})






@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    account_limit = AccountLimit.objects.get(user=user)
    smtp_limit = account_limit.smtp_limit
    sending_limit = account_limit.sending_limit
    try:
        email_verification = EmailAddress.objects.get(user=user)
    except EmailAddress.DoesNotExist:
        email_verification = None
    return render(request, 'profile.html', {'user': user, 'email_verification': email_verification, 'smtp_limit':smtp_limit, 'sending_limit':sending_limit})


@login_required
def leads(request):
    return render(request, 'leads.html')

@login_required
def message_draft(request):
    return render(request, 'message_draft.html')

@login_required
def schedule(request):
    return render(request, 'schedule.html')





