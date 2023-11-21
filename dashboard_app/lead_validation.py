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
# from django.utils.html import escape

def validate_leads(email):
    email = email.lower()
    email = email.strip(" ,.")
    
    # pattern = r'^[\w\.-]+@[\w\.-]+$'
    # pattern = r"^[\w\.'-]+@[\w\.-]+$"
    pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"

    
    if not re.fullmatch (pattern, email):

        # raise ValidationError(f" Remove this, it doesn't look like an email to me: (" + email + ")")
        raise ValidationError(f"looks funny to me. Please remove it:\n ({email})")

