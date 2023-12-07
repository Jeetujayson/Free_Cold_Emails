from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from timezone_field import TimeZoneField
from datetime import time
# from django.db.models import Q, F # Uncomment is Something breaks

# from django.core.exceptions import ValidationError # Uncomment is Something breaks

class SmtpModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    smtp_server = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    imap_server = models.CharField(max_length=255)
    imap_port = models.PositiveIntegerField()
    app_password = models.CharField(max_length=128)  

class LeadList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    list_name = models.CharField(max_length=255)
    uploaded_date = models.DateTimeField(auto_now_add=True)

class LeadEntry(models.Model):
    lead_list = models.ForeignKey(LeadList, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=225) 
    role = models.CharField(max_length=225) 
    column_f = models.CharField(max_length=500)
    column_g = models.CharField(max_length=500)
    column_h = models.CharField(max_length=500) 
    column_i = models.CharField(max_length=500) 
    column_j = models.CharField(max_length=500) 

    # Add other lead attributes here

# class Campaign(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     is_running = models.BooleanField(default=False)
#     campaign_name = models.CharField(max_length=100)
#     sender_email_id = models.ForeignKey(SmtpModel, on_delete=models.CASCADE)
#     lead_list_id = models.ForeignKey(LeadList, on_delete=models.CASCADE)
#     sending_schedule = models.DateTimeField()



class Campaign(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    #change the name to campaign_name
    campaign_name = models.CharField(max_length=255)
    sender_email = models.ForeignKey(SmtpModel, on_delete=models.SET_NULL, null=True)
    lead_list = models.ForeignKey(LeadList, on_delete=models.SET_NULL, null=True)
    is_running = models.BooleanField(default=False)
    timezone = TimeZoneField()  # Use default as per your requirements default='CST'
    daily_limit = models.PositiveIntegerField(default=30)

    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    start_time = models.TimeField(default=time(9, 0))  # Default to 9:00 AM
    end_time = models.TimeField(default=time(17, 0))  # Default to 5:00 PM

    def __str__(self):
        return self.campaign_name


# class CampaignSchedule(models.Model):
#     campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, primary_key=True)
#     sunday = models.BooleanField(default=False)
#     monday = models.BooleanField(default=False)
#     tuesday = models.BooleanField(default=False)
#     wednesday = models.BooleanField(default=False)
#     thursday = models.BooleanField(default=False)
#     friday = models.BooleanField(default=False)
#     saturday = models.BooleanField(default=False)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     def __str__(self):
#         return f"{self.campaign.campaign_name} - Schedule"
        
# class DailySchedule(models.Model):
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
#     day_of_week = models.CharField(max_length=10)  # e.g., 'Monday', 'Tuesday', etc.
#     start_time = models.TimeField()
#     end_time = models.TimeField()

# class EmailDraft(models.Model):
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=255)
#     body = models.TextField()

#     def __str__(self):
#         return f"{self.subject} - {self.campaign}"

# class EmailVariant(models.Model):
#     email_draft = models.ForeignKey(EmailDraft, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)

# class EmailFollowUp(models.Model):
#     variant = models.ForeignKey(EmailVariant, on_delete=models.CASCADE)
#     order = models.PositiveIntegerField()
#     subject = models.CharField(max_length=255)
#     body = models.TextField()
