"""Deployment checks for settings that are unsafe outside local development."""

from django.conf import settings
from django.core.checks import Error, Tags, register


@register(Tags.security, deploy=True)
def check_production_config(app_configs, **kwargs):
    """Fail `manage.py check --deploy` on inherited development defaults."""
    if settings.DEBUG:
        return []

    errors = []
    if settings.SECRET_KEY == settings.DEV_SECRET_KEY:
        errors.append(Error(
            'DJANGO_SECRET_KEY is still set to the development fallback.',
            hint='Generate a unique secret and set DJANGO_SECRET_KEY.',
            id='main_app.E001',
        ))
    if list(settings.ALLOWED_HOSTS) == list(settings.DEFAULT_ALLOWED_HOSTS):
        errors.append(Error(
            'DJANGO_ALLOWED_HOSTS is still set to the local development hosts.',
            hint='Set DJANGO_ALLOWED_HOSTS to the real production hostname(s).',
            id='main_app.E002',
        ))
    return errors
