from django.urls import path, re_path
from Store import views

urlpatterns = [
    re_path("^$", views.login),
    path("register/", views.register),
    path("login/", views.login),
    path("index/", views.index),
    path("blank/", views.blank),
    path("register_store/", views.register_store),
    path("goods_list/", views.list_goods),
    path("add_goods/", views.add_goods),
    re_path(r"^goods/(?P<goods_id>\d+)", views.goods),
    re_path(r"update_goods/(?P<goods_id>\d+)", views.update_goods),
]
