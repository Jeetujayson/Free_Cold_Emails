from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from timezone_field import TimeZoneField
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
    name = models.CharField(max_length=255)
    sender_email = models.ForeignKey(SmtpModel, on_delete=models.SET_NULL, null=True)
    lead_list = models.ForeignKey(LeadList, on_delete=models.SET_NULL, null=True)
    is_running = models.BooleanField(default=False)
    timezone = TimeZoneField(default='CST')  # Use default as per your requirements
    daily_limit = models.PositiveIntegerField()

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
