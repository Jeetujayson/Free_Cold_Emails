from django.contrib.auth import get_user_model
from django.db import models
# from django.db.models import Q, F # Uncomment is Something breaks

# from django.core.exceptions import ValidationError # Uncomment is Something breaks

class SmtpModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    smtp_server = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    app_password = models.CharField(max_length=128)  

    # # Add a check constraint to limit users to 10 emails
    # def save(self, *args, **kwargs):
    #     # Check if the user already has 10 emails associated
    #     if SmtpModel.objects.filter(user=self.user).count() >= 2:
    #         raise ValidationError("You can only add up to 10 emails.")
    #     super(SmtpModel, self).save(*args, **kwargs)

class LeadList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    list_name = models.CharField(max_length=255)
    uploaded_date = models.DateTimeField(auto_now_add=True)

class LeadEntry(models.Model):
    lead_list = models.ForeignKey(LeadList, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=225)  # Adjust the max length as needed
    # Add other lead attributes here