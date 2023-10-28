# import smtplib
# from django.core.exceptions import ValidationError
# from .models import SmtpModel

# def validate_smtp_data(email, smtp_server, port, app_password, user):
#     try:
#         # Check if the email is unique for the user
#         if SmtpModel.objects.filter(user=user, email=email).exists():
#             raise ValidationError("Email must be unique for your account.")

#         # Try to establish a connection to the SMTP server
#         smtp = smtplib.SMTP(smtp_server, port)
#         smtp.ehlo()
#         if not smtp.has_extn("STARTTLS"):
#             raise ValidationError("SMTP server does not support STARTTLS.")
#         smtp.starttls()
#         smtp.ehlo()
#         if not smtp.has_extn("AUTH"):
#             raise ValidationError("SMTP server does not support authentication.")
#         smtp.login(email, app_password)
#         smtp.quit()
#     except (smtplib.SMTPException, smtplib.SMTPResponseException):
#         raise ValidationError("SMTP server, port, or app password is incorrect. Please check your settings.")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
from .models import SmtpModel
from django.core.exceptions import ValidationError
from mysite_app.models import AccountLimit  # Import the AccountLimits model


def validate_smtp_data(email, smtp_server, port, app_password, user):
    # Convert the email to lowercase
    email = email.lower()
    


    try:
        

        print("Try Email Duplicate Check")
        if SmtpModel.objects.filter(email=email).exists():
            print("Try Email IF Duplicate Check")
            raise ValidationError("Duplicate Email, Contact Support.")
            # print("Try Email Duplicate Check Raised Validation Error")
        else:
            # Validate the email address format
            v = validate_email(email)
            print("Validate Email Success")
    except EmailNotValidError as e:
        print("Validate Email Failed")
        raise ValidationError("Validation unsuccessful due to incorrect email address format")
        # return f"Validation unsuccessful due to incorrect email address: {str(e)}"
        
    try:
        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, port)
        print("Validate SMTP SERVER, PORT Success")
    except Exception as e:
        print("Validate SMTP SERVER, PORT Failed")
        raise ValidationError("Validation unsuccessful due to incorrect SMTP SERVER & PORT")
        # return f"Validation unsuccessful due to incorrect SMTP server or port: {str(e)}"

    try:
        # Start TLS for security
        server.starttls()
        print("Validate START TLS Success")
    except Exception as e:
        print("Validate START TLS Failed")
        raise ValidationError("Validation unsuccessful due to incorrect PORT. Use TLS PORT")
        # return f"Validation unsuccessful due to: {str(e)}"

    try:
        # Login to the email account
        server.login(email, app_password)
        print("Validate Email, APP Password Success")
    except Exception as e:
        print(e) # this is working
        print("Validate Email, APP Password Failed")  ####################################################################
        raise ValidationError("Validation unsuccessful due to incorrect email and app password")
        # return f"Validation unsuccessful due to incorrect app password: {str(e)}"

    try:
        # Create a test email message
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = "Sender Email SMTP Verification"
        
        body = "Test Email For SMTP Verification. \nIgnore this email. \nYou don't need to do anything here."
        msg.attach(MIMEText(body, 'plain'))

        # Send the test email to the same address
        server.send_message(msg)
        print("Validate Email Sent Successfully")
        
        # Close the connection to the SMTP server
        server.quit()

    except Exception as e:
        print("Validate General Validation Error")
        raise ValidationError(f"Validation unsuccessful due to: {str(e)}")

    return "Validation successful"
