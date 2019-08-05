from django.urls import path, re_path
from Store import views

urlpatterns = [
    re_path("^$", views.login),
    path("register/", views.register),
    path("login/", views.login),
    path("index/", views.index),
    path("register_store/", views.register_store),
    re_path(r"goods_list/(?P<status>\w+)", views.list_goods),  #商品列表
    path("add_goods/", views.add_goods),  #添加商品
    re_path(r"^goods/(?P<goods_id>\d+)", views.goods),  #详情
    re_path(r"update_goods/(?P<goods_id>\d+)", views.update_goods), #修改商品
    re_path(r'goods_status/(?P<state>\w+)', views.goods_status),  #商品状态
    path("logout/", views.logout),
    path("order_list/", views.order_list),
]



from django.views.decorators.cache import cache_page
urlpatterns += [
    path("base/", cache_page(60*10)(views.base)),
    path("goods_list_api/", views.goods_list_api),  # 商品列表（api渲染）
    path("swv/", views.small_white_views),  # 商品列表（api渲染）

]