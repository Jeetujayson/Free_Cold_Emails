from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from authenticator_app.models import User

# from django.contrib.auth import get_user_model 

def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError("Email address %s already exists, must be unique" % value)

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name  = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(validators=[validate_email_unique], max_length=254, required=True)

##################### To Get Rid of the Instructions on Sign Up Page ######################################
    # password1 = forms.CharField(
    #     label=("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput,
    # )
    # password2 = forms.CharField(
    #     label=("Password confirmation"),
    #     widget=forms.PasswordInput,
    #     strip=False,
    # )

###########################################################
    class Meta:
        model = User
        # model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

        # def __init__(self, *args, **kwargs):
        #     super(CreateAccountForm, self).__init__(*args, **kwargs)
        #     self.fields['username'].widget = forms.HiddenInput()  # Make the username field hidden

        def save(self, commit = True):
            user = super(CreateAccountForm, self).save(commit = False)
            # user.username = self.cleaned_data.get("username", None)
            user.first_name = self.cleaned_data.get("first_name", None)
            user.last_name = self.cleaned_data.get("last_name", None)
            user.email = self.cleaned_data.get("email", None)

            if commit:

                user.save()

            return user

