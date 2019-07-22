from django.urls import path,re_path
from Store import views

urlpatterns = [
    re_path("^$",views.login),
    path("register/",views.register),
    path("login/",views.login),
    path("index/",views.index),
    path("blank",views.blank)
]