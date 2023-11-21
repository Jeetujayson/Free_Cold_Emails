from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress
from django.db.utils import IntegrityError  # Import IntegrityError
from .forms import SmtpForm
from .models import SmtpModel, LeadList, LeadEntry, Campaign
from django.http import JsonResponse  # Import JsonResponse for AJAX responses
import smtplib
from django.contrib import messages
from .smtp_verification import validate_smtp_data
from django.shortcuts import render, redirect
from .forms import SmtpForm
from .smtp_verification import validate_smtp_data
from django.core.exceptions import ValidationError
from mysite_app.models import AccountLimit  # Import the AccountLimits model
import csv
from .lead_validation import validate_leads
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
import time
from django.utils import timezone
import pytz 
# from django.utils.safestring import mark_safe
# from django.utils.html import escape
from django.http import Http404

@login_required
def save_campaign(request, selected_campaign_id=None):
    if request.method == 'POST':
        if selected_campaign_id is not None:
            try:
                campaign = Campaign.objects.get(id=selected_campaign_id, user=request.user)
            except Campaign.DoesNotExist:
                raise Http404("Campaign not found")
            campaign.name = request.POST.get('campaign_name')
            campaign.sender_email_id = request.POST.get('sender_email')
            campaign.lead_list_id = request.POST.get('lead_list')
            campaign.timezone = request.POST.get('timezone')
            campaign.daily_limit = request.POST.get('daily_limit')
            campaign.save()

            messages.success(request, 'Campaign edited successfully.', extra_tags='campaign_success')

    return redirect('campaigns')

    
@login_required
def campaigns(request):
    
    smtp_list = SmtpModel.objects.filter(user=request.user).order_by('id') # Fetch the data from the SmtpModel and LeadList models
    lead_lists = LeadList.objects.filter(user=request.user).order_by('id') # Retrieve the user's lead lists for the dropdown      
    timezones = [(tz, tz) for tz in pytz.common_timezones] # Get a list of timezones
    daily_limit_range = range(1, 51)

    if request.method == 'POST':
        campaign_name = request.POST.get('campaign_name')
        sender_email_id = request.POST.get('sender_email')
        lead_list_id = request.POST.get('lead_list')
        timezone = request.POST.get('timezone')
        daily_limit = request.POST.get('daily_limit')  # Add this line to get daily_limit from the form
        delete_campaign = request.POST.get('delete_campaign')

        if delete_campaign:
            try:
                campaign = Campaign.objects.get(id=delete_campaign, user=request.user)
                campaign.delete()
                print("Deleted Successfully")
                messages.success(request, 'Campaign deleted successfully.', extra_tags='delete_success')
                print("Deleted Success Message Generated ")
                # Clear the session if the list is deleted
                if 'selected_campaign_id' in request.session:
                    if request.session['selected_campaign_id'] == delete_campaign:
                        del request.session['selected_campaign_id']
            except Campaign.DoesNotExist:
                messages.error(request, 'Campaign not found or you do not have permission to delete it.', extra_tags='delete_error')


        else:
            # Fetch the related objects
            sender_email = SmtpModel.objects.get(id=sender_email_id)
            lead_list = LeadList.objects.get(id=lead_list_id)
            if Campaign.objects.filter(user=request.user, name=campaign_name).exists():
                messages.error(request, 'A campaign with this name already exists. Please choose a unique name.', extra_tags='campaign_error')
            else:
                # Create and save the Campaign instance
                campaign = Campaign.objects.create(
                    user=request.user,
                    name=campaign_name,
                    sender_email=sender_email,
                    lead_list=lead_list,
                    timezone=timezone,
                    daily_limit=daily_limit,  # Add this line to set the daily_limit
                )
                messages.success(request, 'Campaign created successfully.', extra_tags='campaign_success')


    campaigns = Campaign.objects.filter(user=request.user).order_by('id') # Retrieve the user's lead lists for the dropdown
    selected_campaign_id = request.GET.get('name')  # Handle lead list selection SUBMIT from the existing dropdown
    if selected_campaign_id:
        try:
            selected_campaign = Campaign.objects.get(id=selected_campaign_id, user=request.user)
            campaign_name = selected_campaign.name
        except Campaign.DoesNotExist:
            selected_campaign = None
            campaign_name = None
    else:
        selected_campaign = None
        campaign_name = None

    # try:
    #     selected_campaign = Campaign.objects.get(id=selected_campaign_id) # Get the campaign name from the selected campaign to display
    #     campaign_name = selected_campaign.campaign_name
    # except:
    #     selected_campaign = None
    #     campaign_name = None
    context = {
            'smtp_list': smtp_list,
            'lead_lists': lead_lists,
            'TIMEZONE_CHOICES': timezones,
            'daily_limit_range': daily_limit_range,
            'campaigns' : campaigns,
            # 'selected_campaign_id' : selected_campaign_id,  # Handle lead list selection SUBMIT from the existing dropdown
            'selected_campaign': selected_campaign,
            'campaign_name' : campaign_name
        }

    return render(request, 'campaigns.html', context)
   

    
@login_required
def append_leads_to_list(request, selected_lead_list, csv_file):

    if csv_file:
        if csv_file.name.endswith(('.csv', '.tsv')):
            decoded_file = csv_file.read().decode('utf-8')
            file_data = csv.reader(decoded_file.splitlines(), delimiter='\t' if csv_file.name.endswith('.tsv') else ',')
            validation_failed = False

            for i, row in enumerate(file_data):
                email = row[0]
                try:
                    validate_leads(email)
                except ValidationError as e:
                    e = (', '.join(e))
                    messages.error(request, f'Row #{i+1} {str(e)}', extra_tags='append_error')
                    validation_failed = True
                    break

                # Create a new LeadEntry and append it to the selected lead list
                lead_entry = LeadEntry(lead_list=selected_lead_list, email=email.lower().strip(" ,."))
                if len(row) > 1:
                    lead_entry.first_name = row[1]
                if len(row) > 2:
                    lead_entry.last_name = row[2]
                if len(row) > 3:
                    lead_entry.company = row[3]
                if len(row) > 4:
                    lead_entry.role = row[4]
                if len(row) > 5:
                    lead_entry.column_f = row[5]
                if len(row) > 6:
                    lead_entry.column_g = row[6]
                if len(row) > 7:
                    lead_entry.column_h = row[7]
                if len(row) > 8:
                    lead_entry.column_i = row[8]
                if len(row) > 9:
                    lead_entry.column_j = row[9]
                # Similar assignments for other fields
                lead_entry.save()

            if not validation_failed:
                messages.success(request, 'Leads appended successfully.', extra_tags='append_success')
        else:
            messages.error(request, 'Invalid file format. Please upload a CSV or TSV file.', extra_tags='append_error')
    else:
        messages.error(request, 'Please select a file to append leads.', extra_tags='append_error')



@login_required
def leads(request):
    show_overlay = True
    if request.method == 'POST':
        show_overlay = True

        csv_file = request.FILES.get('csv_file')
        list_name = request.POST.get('list_name')
        delete_list = request.POST.get('delete_list')

        append_leads = request.POST.get('append_leads')

        if delete_list:
            try:
                lead_list = LeadList.objects.get(id=delete_list, user=request.user)
                lead_list.delete()
                print("Deleted Successfully")
                messages.success(request, 'List deleted successfully.', extra_tags='delete_success')
                print("Deleted Success Message Generated ")
                # Clear the session if the list is deleted
                if 'selected_lead_list_id' in request.session:
                    if request.session['selected_lead_list_id'] == delete_list:
                        del request.session['selected_lead_list_id']
            except LeadList.DoesNotExist:
                messages.error(request, 'List not found or you do not have permission to delete it.', extra_tags='delete_error')
        # Inside your leads view function
        elif append_leads:
            try:
                
                lead_list_id = request.POST.get('lead_list')
                selected_lead_list = LeadList.objects.get(id=lead_list_id, user=request.user)
                # append_leads_to_list(request, selected_lead_list, request.FILES.get('csv_file'))
                append_leads_to_list(request, selected_lead_list, csv_file)


            except ObjectDoesNotExist:
                messages.error(request, 'Selected lead list not found or you do not have permission to append leads to it.', extra_tags='lead_error')

        else:     
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
                            email_validation_failed = False  # Flag to track email validation failure
                            for i, row in enumerate(file_data):
                                # email = escape(row[0])
                                email = row[0]
                                # print(email)
                                try:
                                    validate_leads(email)  # Pass the email to the email validation function
                                except ValidationError as e:
                                    e = (', '.join(e))
                                    # messages.error(request, mark_safe(f'Error in row {i+1}: <br>{e}'), extra_tags='lead_error')
                                    # messages.error(request, f'Row {i+1} : {e}', extra_tags='lead_error')
                                    messages.error(request, f'Row #{i+1} {str(e)}', extra_tags='lead_error')
                                    email_validation_failed = True
                                    break  # Exit the loop on email validation failure
                            if not email_validation_failed:           
                                # Create a new LeadList
                                file_data = csv.reader(decoded_file.splitlines(), delimiter='\t' if csv_file.name.endswith('.tsv') else ',')
                                lead_list = LeadList.objects.create(user=request.user, list_name=list_name)
                                print(file_data)
                                for row in file_data:
                                    lead_entry = LeadEntry(lead_list=lead_list, email=row[0].lower().strip(" ,.")) # Create a new LeadEntry for each row in the uploaded file
                                    if len(row) > 1: # Check if other fields exist in the row before assigning them
                                        lead_entry.first_name = row[1]
                                    if len(row) > 2:
                                        lead_entry.last_name = row[2]
                                    if len(row) > 3:
                                        lead_entry.company = row[3]
                                    if len(row) > 4:
                                        lead_entry.role = row[4]
                                    if len(row) > 5:
                                        lead_entry.column_f = row[5]
                                    if len(row) > 6:
                                        lead_entry.column_g = row[6]
                                    if len(row) > 7:
                                        lead_entry.column_h = row[7]
                                    if len(row) > 8:
                                        lead_entry.column_i = row[8]
                                    if len(row) > 9:
                                        lead_entry.column_j = row[9]
                                    lead_entry.save()
                                messages.success(request, 'File uploaded and processed successfully.', extra_tags='lead_success')
                        else:
                            messages.error(request, 'Invalid file format. Please upload a CSV or TSV file.', extra_tags='lead_error')

    show_overlay = True                     
    lead_lists = LeadList.objects.filter(user=request.user).order_by('id') # Retrieve the user's lead lists for the dropdown
    selected_lead_list_id = request.GET.get('lead_list')  # Handle lead list selection SUBMIT from the existing dropdown
    
    if selected_lead_list_id:
        selected_lead_entries = LeadEntry.objects.filter(lead_list_id=selected_lead_list_id).order_by('id')
        request.session['selected_lead_list_id'] = selected_lead_list_id # Store the selected lead list in the session
    else:
        if 'selected_lead_list_id' in request.session: # Check if there's a selected lead list in the session
            selected_lead_list_id = request.session['selected_lead_list_id']
            selected_lead_entries = LeadEntry.objects.filter(lead_list_id=selected_lead_list_id).order_by('id')
        else:
            selected_lead_entries = None
    
    try:
        #Pagination
        paginator = Paginator(selected_lead_entries, 50) # Show 10 leads per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        paginator = None
        page_number = None
        page_obj = None

    try:
        selected_lead_list = LeadList.objects.get(id=selected_lead_list_id) # Get the list_name from the selected LeadList to display
        list_name = selected_lead_list.list_name
    except:
        selected_lead_list = None
        list_name = None
    # selected_lead_list = LeadList.objects.get(id=selected_lead_list_id) # Get the list_name from the selected LeadList
    # list_name = selected_lead_list.list_name
    # time.sleep(3)
    show_overlay = False
    return render(request, 'leads.html', {'lead_lists': lead_lists, 'list_name': list_name, 'selected_lead_list': selected_lead_list, 'selected_lead_entries': page_obj, 'show_overlay': show_overlay, 'message': messages.get_messages(request)})

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

            user = request.user
            account_limit = AccountLimit.objects.get(user=user)

            if account_limit.smtp_limit > SmtpModel.objects.filter(user=user).count():
   
                if form.is_valid():
         
                    user = request.user
                    smtp_data = form.save(commit=False) # creates an instance of the form
                    smtp_data.user = request.user
    
                    try:

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
  
                error_message = "You have reached the maximum allowed SMTP configurations."
                linked_emails = SmtpModel.objects.filter(user=request.user)
                return render(request, 'db.html', {'linked_emails': linked_emails, 'error_message': error_message, 'show_overlay': show_overlay,})

        linked_emails = SmtpModel.objects.filter(user=request.user)

    else:

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
def schedule(request):
    return render(request, 'schedule.html')





