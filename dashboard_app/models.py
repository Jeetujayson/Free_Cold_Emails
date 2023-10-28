from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F
# from django.contrib.auth.hashers import make_password
# Create your models here.
from django.core.exceptions import ValidationError

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

