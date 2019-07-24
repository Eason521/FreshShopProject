import json

from django import template

register = template.Library()


@register.filter(name="validcookie")
def validcookie(value):
    username = json.loads(value)
    return username
