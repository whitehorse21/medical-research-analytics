import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-h1r=%__^y_g@ihdvskpj3*ddvazml=x__ga=6!u6395*0=3yvn'
DEBUG = True
 
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app", ".now.sh", ".ondigitalocean.app"]

# Detect if we're in production (Vercel)
IS_PRODUCTION = os.getenv('VERCEL') or any(host in str(os.getenv('ALLOWED_HOSTS', '')) for host in ['.vercel.app', '.now.sh'])

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "https://medical-research-analytics-ntqn.vercel.app",  # Add your Vercel frontend URL
]
# Add any additional Vercel URLs from environment
if os.getenv('FRONTEND_URL'):
    CSRF_TRUSTED_ORIGINS.append(os.getenv('FRONTEND_URL'))

CSRF_COOKIE_SECURE = IS_PRODUCTION  # True for HTTPS in production
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'None' if IS_PRODUCTION else 'Lax'  # None for cross-origin cookies
CSRF_USE_SESSIONS = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "core",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.DisableCSRFForAPI",  # Disable CSRF for API before CSRF middleware
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "medresearch.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "medresearch.wsgi.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

DATABASES = {
  "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins in development
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5174',
    'https://medical-research-analytics-ntqn.vercel.app',  # Add your Vercel frontend URL
]
# Add any additional Vercel URLs from environment
if os.getenv('FRONTEND_URL'):
    CORS_ORIGIN_WHITELIST.append(os.getenv('FRONTEND_URL'))

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    'http://127.0.0.1:5173', 
    'http://127.0.0.1:5174',
    'https://medical-research-analytics-ntqn.vercel.app',  # Add your Vercel frontend URL
]
if os.getenv('FRONTEND_URL'):
    CORS_ALLOWED_ORIGINS.append(os.getenv('FRONTEND_URL'))

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    # Disable CSRF for API views (handled by CORS and authentication)
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# Exempt API views from CSRF
CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

# Session cookie configuration for cross-origin requests
SESSION_COOKIE_SECURE = IS_PRODUCTION  # True for HTTPS in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'None' if IS_PRODUCTION else 'Lax'  # None for cross-origin cookies
SESSION_COOKIE_AGE = 86400  # 24 hours


