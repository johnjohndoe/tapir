"""
Django settings for tapir project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import email.utils
import os
from datetime import timedelta
from pathlib import Path

import celery.schedules
import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY", default="fl%20e9dbkh4mosi5$i$!5&+f^ic5=7^92hrchl89x+)k0ctsn"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", cast=list, default=["*"])

ENABLE_SILK_PROFILING = False
ENABLE_API = env("ENABLE_API", cast=bool, default=False)

# Application definition
INSTALLED_APPS = [
    # Must come before contrib.auth to let the custom templates be discovered for auth views
    "tapir.accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django_bootstrap5",
    "tapir.core",
    "tapir.log",
    "tapir.shifts",
    "tapir.utils",
    "tapir.coop",
    "tapir.welcomedesk",
    "tapir.statistics",
    "tapir.financingcampaign",
    "django_tables2",
    "django_filters",
    "django_select2",  # For autocompletion in form fields
    "phonenumber_field",
    "django_extensions",
    "chartjs",
]

if ENABLE_SILK_PROFILING:
    INSTALLED_APPS.append("silk")

if ENABLE_API:
    INSTALLED_APPS.append("rest_framework")
    INSTALLED_APPS.append("rest_framework_simplejwt")
    INSTALLED_APPS.append("tapir.api")

if DEBUG and ENABLE_API:
    INSTALLED_APPS.append("corsheaders")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "tapir.welcomedesk.middleware.WelcomeDeskPermsMiddleware",
    "tapir.accounts.models.language_middleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if ENABLE_SILK_PROFILING:
    MIDDLEWARE = ["silk.middleware.SilkyMiddleware"] + MIDDLEWARE

if DEBUG and ENABLE_API:
    MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE

    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://localhost.*$",
        r"^http://127.0.0.1.*$",
    ]
    CORS_URLS_REGEX = r"^/api/.*$"

ROOT_URLCONF = "tapir.urls"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "tapir/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tapir.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": env.db(default="postgresql://tapir:tapir@db:5432/tapir"),
    "ldap": env.db_url(
        "LDAP_URL", default="ldap://cn=admin,dc=supercoop,dc=de:admin@openldap"
    ),
}

DATABASE_ROUTERS = ["ldapdb.router.Router"]

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_BEAT_SCHEDULE = {
    "send_shift_reminders": {
        "task": "tapir.shifts.tasks.send_shift_reminders",
        "schedule": celery.schedules.crontab(
            hour="*/2", minute=5
        ),  # Every two hours five after the hour
    },
    "apply_shift_cycle_start": {
        "task": "tapir.shifts.tasks.apply_shift_cycle_start",
        "schedule": celery.schedules.crontab(hour="*/2", minute=20),
    },
    "send_accounting_recap": {
        "task": "tapir.coop.tasks.send_accounting_recap",
        "schedule": celery.schedules.crontab(hour=12, minute=0, day_of_week="sunday"),
    },
    "generate_shifts": {
        "task": "tapir.shifts.tasks.generate_shifts",
        "schedule": celery.schedules.crontab(minute=0, hour=0),
    },
    "update_purchase_tracking_list": {
        "task": "tapir.accounts.tasks.update_purchase_tracking_list",
        "schedule": celery.schedules.crontab(minute=0, hour=23),
    },
    "run_freeze_checks": {
        "task": "tapir.shifts.tasks.run_freeze_checks",
        "schedule": celery.schedules.crontab(minute=0, hour=1),
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
PASSWORD_RESET_TIMEOUT = (
    7776000  # 90 days, so that the welcome emails stay valid for long enough
)


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True

EMAIL_ADDRESS_MEMBER_OFFICE = "mitglied@supercoop.de"
EMAIL_ADDRESS_ACCOUNTING = "accounting@supercoop.de"
EMAIL_ADDRESS_MANAGEMENT = "contact@supercoop.de"
EMAIL_ADDRESS_SUPERVISORS = "aufsichtsrat@supercoop.de"

# django-environ EMAIL_URL mechanism is a bit hairy with passwords with slashes in them, so use this instead
EMAIL_ENV = env("EMAIL_ENV", default="dev")
if EMAIL_ENV == "dev" or EMAIL_ENV == "test":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_ENV == "prod":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST", default="smtp-relay.gmail.com")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default=EMAIL_ADDRESS_MEMBER_OFFICE)
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True


COOP_NAME = "SuperCoop Berlin"
COOP_FULL_NAME = "SuperCoop Berlin eG"
COOP_STREET = "Oudenarder Straße 16"
COOP_PLACE = "13347 Berlin"
FROM_EMAIL_MEMBER_OFFICE = f"{COOP_NAME} Mitgliederbüro <{EMAIL_ADDRESS_MEMBER_OFFICE}>"
DEFAULT_FROM_EMAIL = FROM_EMAIL_MEMBER_OFFICE


# DJANGO_ADMINS="Blake <blake@cyb.org>, Alice Judge <alice@cyb.org>"
ADMINS = tuple(email.utils.parseaddr(x) for x in env.list("DJANGO_ADMINS", default=[]))
# Crash emails will come from this address.
# NOTE(Leon Handreke): I don't know if our Google SMTP will reject other senders, so play it safe.
SERVER_EMAIL = env("SERVER_EMAIL", default=EMAIL_ADDRESS_MEMBER_OFFICE)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

SELECT2_JS = "core/select2/4.0.13/js/select2.min.js"
SELECT2_CSS = "core/select2/4.0.13/css/select2.min.css"
SELECT2_I18N_PATH = "core/select2/4.0.13/js/i18n"

WEASYPRINT_BASEURL = "/"

REG_PERSON_BASE_DN = "ou=people,dc=supercoop,dc=de"
REG_PERSON_OBJECT_CLASSES = ["inetOrgPerson", "organizationalPerson", "person"]
REG_GROUP_BASE_DN = "ou=groups,dc=supercoop,dc=de"
REG_GROUP_OBJECT_CLASSES = ["groupOfNames"]

PERMISSION_SHIFTS_MANAGE = "shifts.manage"
PERMISSION_SHIFTS_EXEMPTIONS = "shifts.exemptions"
PERMISSION_COOP_VIEW = "coop.view"
PERMISSION_COOP_MANAGE = "coop.manage"
PERMISSION_COOP_ADMIN = "coop.admin"
PERMISSION_ACCOUNTS_VIEW = "accounts.view"
PERMISSION_ACCOUNTS_MANAGE = "accounts.manage"
PERMISSION_WELCOMEDESK_VIEW = "welcomedesk.view"
PERMISSION_ACCOUNTING_VIEW = "accounting.view"
PERMISSION_ACCOUNTING_MANAGE = "accounting.manage"

# Groups are stored in the LDAP tree
GROUP_VORSTAND = "vorstand"
GROUP_MEMBER_OFFICE = "member-office"
GROUP_SHIFT_MANAGER = "shift-manager"
GROUP_ACCOUNTING = "accounting"

LDAP_GROUPS = [
    GROUP_VORSTAND,
    GROUP_MEMBER_OFFICE,
    GROUP_SHIFT_MANAGER,
    GROUP_ACCOUNTING,
]

PERMISSIONS = {
    PERMISSION_SHIFTS_MANAGE: [
        GROUP_VORSTAND,
        GROUP_MEMBER_OFFICE,
        GROUP_SHIFT_MANAGER,
    ],
    PERMISSION_SHIFTS_EXEMPTIONS: [GROUP_VORSTAND, GROUP_MEMBER_OFFICE],
    PERMISSION_COOP_VIEW: [GROUP_VORSTAND, GROUP_MEMBER_OFFICE, GROUP_ACCOUNTING],
    PERMISSION_COOP_MANAGE: [GROUP_VORSTAND, GROUP_MEMBER_OFFICE],
    PERMISSION_COOP_ADMIN: [GROUP_VORSTAND],
    PERMISSION_ACCOUNTS_VIEW: [GROUP_VORSTAND, GROUP_MEMBER_OFFICE, GROUP_ACCOUNTING],
    PERMISSION_ACCOUNTS_MANAGE: [GROUP_VORSTAND, GROUP_MEMBER_OFFICE],
    PERMISSION_WELCOMEDESK_VIEW: [GROUP_VORSTAND, GROUP_MEMBER_OFFICE],
    PERMISSION_ACCOUNTING_VIEW: [GROUP_VORSTAND, GROUP_MEMBER_OFFICE, GROUP_ACCOUNTING],
    PERMISSION_ACCOUNTING_MANAGE: [GROUP_VORSTAND, GROUP_ACCOUNTING],
}

# Permissions granted to client presenting a given SSL client cert. Currently used for the welcome desk machines.
LDAP_WELCOME_DESK_ID = "CN=welcome-desk.members.supercoop.de,O=SuperCoop Berlin eG,C=DE"
CLIENT_PERMISSIONS = {
    LDAP_WELCOME_DESK_ID: [
        PERMISSION_WELCOMEDESK_VIEW,
    ]
}

AUTH_USER_MODEL = "accounts.TapirUser"
LOGIN_REDIRECT_URL = "accounts:user_me"

SITE_URL = env("SITE_URL", default="http://127.0.0.1:8000")

PHONENUMBER_DEFAULT_REGION = "DE"

LOCALE_PATHS = [os.path.join(BASE_DIR, "tapir/translations/locale")]

if ENABLE_SILK_PROFILING:
    SILKY_PYTHON_PROFILER = True
    SILKY_META = True
    SILKY_PROFILE_DIR = "silk_profiling"

if ENABLE_API:
    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ),
    }

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
        "REFRESH_TOKEN_LIFETIME": timedelta(weeks=12),
    }
