from django.urls import path,include
from Buyer.views import *


urlpatterns = [
    path("index/",index),
    path("register/",register),
    path("login/",login),
]

urlpatterns += [
    path("base/",base),
]