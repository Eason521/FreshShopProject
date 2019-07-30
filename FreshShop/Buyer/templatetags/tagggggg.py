from django import template
from Store.models import *
from Buyer.models import *

register = template.Library()


@register.filter(name="validcookie")
def goods_online(value):
    goods = value.goods_set.all()
    return goods

@register.filter(name="cart")
def buy_cart(value): #goods.goods_id
    goods = Goods.objects.filter(id=value).first()
    return goods.goods_image
