from django import template
from django.utils.translation import get_language

from ..i18n import FR

register = template.Library()


@register.filter(name='tr')
def tr(value):
    """Translate an English UI string into the active language."""
    if not value:
        return value
    if get_language() == 'fr' and value in FR:
        return FR[value]
    return value