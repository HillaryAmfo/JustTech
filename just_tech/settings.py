"""
Django settings for just_tech project.

Sensitive/deployment-specific values are read from environment variables.
Local development may use a `.env` file (see .env.example) — it is loaded
automatically if present. Never commit a real secret to the repository.
"""

import os
from pathlib import Path
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(path):
    """Load NAME=VALUE lines from a simple .env file without external dependencies.

    Existing environment variables always win (values already set are not
    overwritten).
    """
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


_load_env_file(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
# Provide DJANGO_SECRET_KEY in production. The fallback below exists only so a
# fresh checkout can run the dev server out of the box — never use it online.
# `manage.py check --deploy` fails when these defaults reach production.
DEV_SECRET_KEY = 'django-insecure-dev-key-change-me'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', DEV_SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG=True locally, DEBUG=False in production (e.g. DJANGO_DEBUG=false).
DEBUG = os.environ.get('DJANGO_DEBUG', 'true').lower() == 'true'

DEFAULT_ALLOWED_HOSTS = ('localhost', '127.0.0.1')
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'DJANGO_ALLOWED_HOSTS', ','.join(DEFAULT_ALLOWED_HOSTS),
    ).split(',')
    if host.strip()
]
# Add the real production domain to DJANGO_ALLOWED_HOSTS at deploy time,
# e.g. DJANGO_ALLOWED_HOSTS=justtech.example,www.justtech.example

# Trusted origins for unsafe HTTP methods over HTTPS. Add the production origin
# at deploy time, e.g. DJANGO_CSRF_TRUSTED_ORIGINS=https://justtech.example
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

# Canonical site URL used for canonical links and Open Graph meta tags.
# Leave unset during development (the request host is used automatically); set
# e.g. SITE_URL=https://justtech.example at deploy time.
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')

# Application definition
# Email
# -----
# In development mail is printed to the console so password-reset links are
# visible without a real SMTP server. Configure DJANGO_EMAIL_HOST / *_PORT etc.
# at deploy time; a real provider (e.g. Mailgun, SendGrid, Postmark) is
# strongly recommended for production.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'true').lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'JustTech <noreply@justtech.com>')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'main_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'just_tech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main_app.context_processors.site_settings',
                'main_app.context_processors.language',
            ],
        },
    },
]

WSGI_APPLICATION = 'just_tech.wsgi.application'

# Database
# ---------
# Default: SQLite (excellent for development, fine for modest deployments).
# Production limitation: SQLite serialises writes and is not suited to a
# high-concurrency multi-process web deployment.
#
# A production database can be enabled without code changes by providing
# DJANGO_DATABASE_URL (see .env.example). No driver package is installed in
# this project — the relevant driver (e.g. psycopg[binary] for PostgreSQL) must
# be added to requirements.txt before deploying with a database.
def _database_from_url(url):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.hostname:
        return None
    engine_map = {
        'postgres': 'django.db.backends.postgresql',
        'postgresql': 'django.db.backends.postgresql',
        'mysql': 'django.db.backends.mysql',
        'sqlite': 'django.db.backends.sqlite3',
    }
    engine = engine_map.get(parsed.scheme.lower())
    if engine is None:
        return None
    if parsed.scheme.lower() == 'sqlite':
        return {'ENGINE': engine, 'NAME': parsed.path or ':memory:'}
    return {
        'ENGINE': engine,
        'NAME': parsed.path.lstrip('/'),
        'USER': parsed.username,
        'PASSWORD': parsed.password,
        'HOST': parsed.hostname,
        'PORT': parsed.port,
    }


DATABASE_URL = os.environ.get('DJANGO_DATABASE_URL')
DATABASES = {
    'default': _database_from_url(DATABASE_URL)
    if DATABASE_URL
    else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en'

# Site languages — picked up by the EN/FR navbar switch, which sets the
# ``lang`` cookie that LocaleMiddleware reads as ``LANGUAGE_COOKIE_NAME``.
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
]
LANGUAGE_COOKIE_NAME = 'lang'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Production location for `python manage.py collectstatic --noinput`.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (user uploads)
# The current models store image URLs, not uploaded files, so nothing is
# actually uploaded today. In production, /media/ should be served by the
# hosting or storage platform — Django itself should not serve uploads.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
# Always-on, safe for both HTTP and HTTPS:
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# HTTPS-only hardening. Enable when the site is served over HTTPS.
# e.g. DJANGO_HTTPS=true in the production environment (NOT on local HTTP dev).
HTTPS_ENABLED = os.environ.get('DJANGO_HTTPS', 'false').lower() == 'true'
if HTTPS_ENABLED:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False