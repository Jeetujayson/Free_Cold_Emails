from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.db.utils import IntegrityError  # Import IntegrityError
from .forms import SmtpForm
from .models import SmtpModel, LeadList, LeadEntry 
from django.http import JsonResponse  # Import JsonResponse for AJAX responses
import smtplib
from django.contrib import messages
from .smtp_verification import validate_smtp_data
from django.shortcuts import render, redirect
from .forms import SmtpForm
# from .models import SmtpModel
from .smtp_verification import validate_smtp_data
from django.core.exceptions import ValidationError
from mysite_app.models import AccountLimit  # Import the AccountLimits model

import csv


@login_required
def leads(request):
    # selected_lead_list_id = None
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        list_name = request.POST.get('list_name')
        if not list_name:
            messages.error(request, 'Please provide a list name.', extra_tags='lead_error')
        elif not csv_file:
            messages.error(request, 'Please select a file to upload.', extra_tags='lead_error')
        else:
            if not list_name.isalnum():
                messages.error(request, 'List name should contain only alphanumeric characters.', extra_tags='lead_error')
            else:
                if LeadList.objects.filter(user=request.user, list_name=list_name).exists():
                    messages.error(request, 'A list with this name already exists. Please choose a unique name.', extra_tags='lead_error')
                else:
                    if csv_file.name.endswith(('.csv', '.tsv')):
                        decoded_file = csv_file.read().decode('utf-8')
                        file_data = csv.reader(decoded_file.splitlines(), delimiter='\t' if csv_file.name.endswith('.tsv') else ',')
                        # Create a new LeadList
                        lead_list = LeadList.objects.create(user=request.user, list_name=list_name)
                        for row in file_data:
                            lead_entry = LeadEntry(lead_list=lead_list, email=row[0]) # Create a new LeadEntry for each row in the uploaded file
                            # Check if other fields exist in the row before assigning them
                            if len(row) > 1:
                                lead_entry.first_name = row[1]
                            if len(row) > 2:
                                lead_entry.last_name = row[2]
                            if len(row) > 3:
                                lead_entry.phone = row[3]
                            lead_entry.save()
                        messages.success(request, 'File uploaded and processed successfully.', extra_tags='lead_success')
                    else:
                        messages.error(request, 'Invalid file format. Please upload a CSV or TSV file.', extra_tags='lead_error')
    else: # GET Request Code
        selected_lead_list_id = request.GET.get('lead_list')  # Handle lead list selection SUBMIT from the existing dropdown

        # if selected_lead_list_id:
            
        #     request.session['selected_lead_list_id'] = selected_lead_list_id # Store the selected lead list in the session
        # else:
        #     print("Nothing Selected")

        lead_lists = LeadList.objects.filter(user=request.user) # Retrieve the user's lead lists for the dropdown
        print("Selected Lead List ID:", selected_lead_list_id)


        if selected_lead_list_id:
            selected_lead_entries = LeadEntry.objects.filter(lead_list_id=selected_lead_list_id)
            request.session['selected_lead_list_id'] = selected_lead_list_id # Store the selected lead list in the session
        else:

                # Check if there's a selected lead list in the session
            if 'selected_lead_list_id' in request.session:
                selected_lead_list_id = request.session['selected_lead_list_id']
                selected_lead_entries = LeadEntry.objects.filter(lead_list_id=selected_lead_list_id)
            else:
                selected_lead_entries = None
    return render(request, 'leads.html', {'lead_lists': lead_lists, 'selected_lead_entries': selected_lead_entries, 'message': messages.get_messages(request)})



# @login_required
# def leads(request):
#     if request.method == 'POST':
#         csv_file = request.FILES.get('csv_file')
        
#         if csv_file:
#             # Process the uploaded file
#             if csv_file.name.endswith(('.csv', '.tsv')):
#                 decoded_file = csv_file.read().decode('utf-8')
#                 file_data = csv.reader(decoded_file.splitlines(), delimiter='\t' if csv_file.name.endswith('.tsv') else ',')
                
                
#                 for row in file_data:
#                     # Print each row to the console or perform other operations
#                     print(row)
#                     print(', '.join(row))
                
#                 # Provide feedback to the user
#                 messages.success(request, 'File uploaded and processed successfully.')


#             else:
#                 messages.error(request, 'Invalid file format. Please upload a CSV or TSV file.')

#         else:
#             # Handle the case where no file was selected
#             messages.error(request, 'Please select a file to upload.')

#     # return render(request, 'leads.html')
#     return render(request, 'leads.html', {'message': messages.get_messages(request)})






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

@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    account_limit = AccountLimit.objects.get(user=user)
    smtp_limit = account_limit.smtp_limit
    sending_limit = account_limit.sending_limit
    try:
        # primary_email = EmailAddress.objects.get(user=user, primary=True)
        email_verification = EmailAddress.objects.get(user=user, primary=True)
    except EmailAddress.DoesNotExist:
        email_verification = None
    return render(request, 'profile.html', {'user': user, 'email_verification': email_verification, 'smtp_limit':smtp_limit, 'sending_limit':sending_limit})




@login_required
def message_draft(request):
    return render(request, 'message_draft.html')

@login_required
def schedule(request):
    return render(request, 'schedule.html')





