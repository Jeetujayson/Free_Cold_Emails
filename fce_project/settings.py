"""
Django settings for fce_project project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(cggagk%h&=##(ha^8&0$#iqx4b3ot!ud0nwo=6l*4ljtit7^m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.40.3']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth', #Allauth Documentation Requirement
    'allauth.account', #Allauth Documentation Requirement
    'allauth.socialaccount',#Allauth Documentation Requirement
    'mysite_app',
    'dashboard_app',



]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "allauth.account.middleware.AccountMiddleware", #Allauth Documentation Requirement
    
]

# Provider specific settings #Allauth Documentation Requirement
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

ROOT_URLCONF = 'fce_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, 'mysite_app', 'templates')],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fce_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# Additional directories to search for static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'mysite_app', 'static'), 
                    os.path.join(BASE_DIR, 'dashboard_app', 'static')
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field




#Allauth Documentation Requirement
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend", #Allauth Documentation Requirement
    'allauth.account.auth_backends.AuthenticationBackend', #Allauth Documentation Requirement


]

SITE_ID = 1


############### Custome Profile ###################################
# LOGIN_REDIRECT_URL = 'db_view'  # This should match the name you specified in your URL pattern


# ACCOUNT_PROFILE = 'dashboard_app.views.profile'
ACCOUNT_PROFILE = 'dashboard_app.views'

################### Experimental ###########################
AUTH_USER_MODEL = 'mysite_app.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

######################## Working #######################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None # Very Important - Field Does Not Exist Error If Deleted

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
# SESSION_COOKIE_AGE: 1209600 # seconds (2 weeks)
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_UNIQUE_EMAIL = True    # Optional I think. Only needed if username is active


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use 587 for TLS or 465 for SSL
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # Set to True for SSL
EMAIL_HOST_USER = config('DB_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DB_HOST_USER')

###########################################################################

ACCOUNT_FORMS = {
    'signup': 'mysite_app.forms.CustomSignupForm',
}

########################## TODAY #########################################
ACCOUNT_RATE_LIMITS = {
    # Change password view (for users already logged in)
    "change_password": "5/m",
    # Email management (e.g. add, remove, change primary)
    "manage_email": "10/m",
    # Request a password reset, global rate limit per IP
    "reset_password": "1/m",
    # Rate limit measured per individual email address
    "reset_password_email": "1/m",
    # Password reset (the view the password reset email links to).
    "reset_password_from_key": "20/m",
    # Signups.
    "signup": "20/m",
    # NOTE: Login is already protected via `ACCOUNT_LOGIN_ATTEMPTS_LIMIT`
}



# Set the maximum number of login attempts
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3

# Set the maximum number of signup attempts
ACCOUNT_SIGNUP_ATTEMPTS_LIMIT = 3


# Set the expiration period for email confirmation links (in days)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

# Set the duration of lockout for login attempts (in seconds)
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutes

# Set the expiration period for email confirmation links (in days)
ACCOUNT_EMAIL_VERIFICATION_EXPIRE_DAYS = 3

# # Automatically log in the user after email confirmation
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True


