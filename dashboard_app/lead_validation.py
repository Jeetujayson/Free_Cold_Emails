# from email_validator import validate_email, EmailNotValidError

# def validate_leads(leads):
#     for lead in leads:
#         email = lead[0]  # assuming the email is in the first column
#         try:
#             # validate and get info
#             v = validate_email(email)
#             print(f"{email} is valid")
#         except EmailNotValidError as e:
#             # email is not valid, exception message is human-readable
#             print(f"Invalid email in row {lead}: {str(e)}")


# 

import re
from django.core.exceptions import ValidationError

def validate_leads(email):
    pattern = r'^[\w\.-]+@[\w\.-]+$'
    if not re.match(pattern, email):
        raise ValidationError("Remove this, it doesn't look like an email to me: (" + email + ")")
