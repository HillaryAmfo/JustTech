from django.conf import settings
from django.db import DatabaseError
from django.utils import translation

from .i18n import SUPPORTED_LANGS
from .models import SiteSettings


def language(request):
    """Expose the active site language (from the ``lang`` cookie)."""
    lang = translation.get_language()
    if lang not in SUPPORTED_LANGS:
        lang = settings.LANGUAGE_CODE or 'en'
    return {'LANG': lang}


def site_settings(request):
    # Error pages must still render when the database is the reason for the
    # failure. A missing/unavailable SiteSettings row is never fatal.
    try:
        settings_obj = SiteSettings.objects.first()
    except DatabaseError:
        settings_obj = None

    site_url = getattr(settings, 'SITE_URL', '').rstrip('/')
    if not site_url:
        site_url = f'{"https" if request.is_secure() else "http"}://{request.get_host()}'

    return {
        'site_settings': settings_obj,
        'debug': settings.DEBUG,
        'SITE_URL': site_url,
    }
