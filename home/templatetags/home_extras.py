from django import template
from django.conf import settings

register = template.Library()


# Регистрируем тег, с помощью которого будем получать атрибуты из файла settings.SITE_URL
@register.simple_tag
def get_attribute(name):
    return getattr(settings, name, "")