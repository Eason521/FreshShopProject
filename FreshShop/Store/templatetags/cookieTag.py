import json

from django import template
from Store import models

register = template.Library()


@register.filter(name="validcookie")
def validcookie(value):
    username = json.loads(value)
    return username


@register.filter(name="goods_type_name")
def goods_type_name(value):
    goods_type = models.GoodsType.objects.filter(id=value).first()

    return goods_type.name