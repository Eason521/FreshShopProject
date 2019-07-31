from django.urls import path,re_path,include
from Buyer.views import *

urlpatterns = [
    path("index/",index),
    path("register/",register),
    path("login/",login),
    re_path(r"goods_list/",goods_list),
    path("goods_detail/", goods_detail),
    path("place_order/", place_order),
    path("add_cart/", add_cart),
    path("cart/", cart),
    path("del_cart_goods/", del_cart_goods),
    path("cart_order/", cart_order),
    path("user_center_order/", user_center_order),
    path("user_center_info/", user_center_info),
    path("user_center_site/", user_center_site),

    path("getProvince/", getProvince),
    path("getCity/", getCity),
    path("getDistrict/", getDistrict),




]

urlpatterns += [
    path("base/",base),
    path("pay_order/", pay_order),
    path("pay_result/", pay_result),
]