from django.urls import path,re_path,include
from Buyer.views import *

urlpatterns = [
    path("index/",index),
    path("register/",register),
    path("login/",login),
    re_path(r"goods_list/",goods_list),
    # re_path(r"goods_detail/",goods_detail),
    path("pay_order/", pay_order),
    path("goods_detail/", goods_detail),
    path("pay_result/", pay_result),
]

urlpatterns += [
    path("base/",base),
]