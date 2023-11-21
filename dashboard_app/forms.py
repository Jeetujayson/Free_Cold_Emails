from django import forms
from .models import SmtpModel
from .smtp_verification import validate_smtp_data
from django.core.exceptions import ValidationError

class SmtpForm(forms.ModelForm):
    class Meta:
        model = SmtpModel
        fields = ['email', 'smtp_server', 'port', 'imap_server', 'imap_port', 'app_password']
        

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # Convert the email to lowercase
        cleaned_data['email'] = email.lower()

        smtp_server = cleaned_data.get('smtp_server')
        port = cleaned_data.get('port')
        imap_server = cleaned_data.get('imap_server')
        imap_port = cleaned_data.get('imap_port')
        app_password = cleaned_data.get('app_password')
        user = cleaned_data.get('user')

        try:
            print("Try Form Validation")
            validate_smtp_data(email, smtp_server, port, imap_server, imap_port, app_password, user)
            print("Tried Form Validation")
            return cleaned_data
        except ValidationError as e:
            print("Let's see")
            raise ValidationError("ERROR: " + str((', '.join(e))))

        