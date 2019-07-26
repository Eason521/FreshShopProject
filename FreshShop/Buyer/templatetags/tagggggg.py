from django import template
from Store import models

register = template.Library()


@register.filter(name="validcookie")
def goods_online(value):
    goods = value.goods_set.all()
    return goods