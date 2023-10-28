from allauth.account.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError
from mysite_app.models import User, AccountLimit# Import your custom User model here

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()  # Convert to lowercase

        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please choose another email.")
        
        return email

    def save(self, request):
        # Call the parent class's save method to create the user
        user = super(CustomSignupForm, self).save(request)

        # Create an associated AccountLimits instance with initial values
        AccountLimit.objects.create(user=user, smtp_limit=1, sending_limit=1000)

        return user