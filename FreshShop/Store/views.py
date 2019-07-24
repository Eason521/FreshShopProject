#coding:utf-8
import hashlib
import json

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from Store import models


# Create your views here.
def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        # s_user = json.loads(s_user)
        if c_user and s_user:
            username = json.loads(c_user)
            if username == s_user:
                user = models.Seller.objects.filter(username=username).first()
                if user:
                    return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/store/login/")
    return inner


def setPassword(password):  # 加密函数
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()


def register(request):  # 注册函数
    result={"info":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        c_password = request.POST.get("confirm_password")
        if username and password and c_password:
            sql_username = models.Seller.objects.filter(username=username).first()
            if sql_username:
                result["info"]="用户已存在"
                return render(request, "store/register.html", locals())

            else:
                if password == c_password:
                    models.Seller.objects.create(
                        username=username,
                        password=setPassword(password)
                    )
                    return HttpResponseRedirect("/store/login/")
                else:
                    result["info"] = "两次密码不相等"
        else:
            result["info"] = "注册信息不能为空"
    return render(request, "store/register.html",locals())


def login(request):  # 登录函数
    response = render(request, "store/login.html")
    response.set_cookie("login_form","login_page")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            sql_username = models.Seller.objects.filter(username=username).first()
            if sql_username:
                cookie=request.COOKIES.get("login_form")
                hex_password = setPassword(password)
                if sql_username.password == hex_password and cookie=="login_page":
                    u = json.dumps(username)
                    response = HttpResponseRedirect("/store/index/")
                    response.set_cookie("username", u)
                    response.set_cookie("user_id", sql_username.id) #cookie提供用户id方便其他功能查询

                    request.session["username"] = username
                    return response
    return response


@loginValid
def index(request):
    username = request.COOKIES.get("username")
    if username:
        u = json.loads(username)
        user_id = request.COOKIES.get("user_id")
        if user_id:
            user_id = int(user_id)
        else:
            user_id = 0
            # 通过用户查询店铺是否存在(店铺和用户通过用户的id进行关联)
        store = models.Store.objects.filter(user_id=user_id).first()
        if store:
            is_store = 1
        else:
            is_store = 0
        return render(request, "store/index.html",locals())
    return HttpResponseRedirect("/store/login/")


@loginValid
def register_store(request):
    username = request.COOKIES.get("username")
    if username:
        u = json.loads(username)

    type_list = models.StoreType.objects.all()
    if request.method == "POST":
        store_name = request.POST.get("store_name")
        store_address = request.POST.get("store_address")
        store_description = request.POST.get("store_description")
        store_phone = request.POST.get("store_phone")
        store_money = request.POST.get("store_money")

        user_id =int(request.COOKIES.get("user_id")) #通过cookie来得到user_id
        type_list = request.POST.get("type") #通过request.post得到类型，但是是一个列表

        store_logo = request.FILES.get("store_logo") #通过request.FILES得到
        # 保存非多对多数据
        store = models.Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo  # django1.8之后图片可以直接保存
        store.save()  # 保存，生成了数据库当中的一条数据
        # 在生成的数据当中添加多对多字段。
        for i in type_list:  # 循环type列表，得到类型id
            store_type = models.StoreType.objects.get(id=i)  # 查询类型数据
            store.type.add(store_type)  # 添加到类型字段，多对多的映射表
        store.save()  # 保存数据
        return HttpResponseRedirect("/store/index/")
    return render(request,"store/register_store.html",locals())


@loginValid
def add_goods(request):
    username = request.COOKIES.get("username")
    if username:
        u = json.loads(username)
    if request.method == "POST":
        #获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.POST.get("goods_store")
        goods_image = request.FILES.get("goods_image")
        #开始保存数据
        goods = models.Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()
        #保存多对多数据
        goods.store_id.add(
            models.Store.objects.get(id = int(goods_store))
        )
        goods.save()
        return HttpResponseRedirect("/store/goods_list/")
    return render(request,"store/add_goods.html",locals())


# @loginValid
# def goods_list(request):
#     username = request.COOKIES.get("username")
#     if username:
#         u = json.loads(username)
#     goods_list = models.Goods.objects.all()
#     return render(request,"store/goods_list.html",{"goods_list":goods_list,"u":u})


@loginValid
def list_goods(request):
    username = request.COOKIES.get("username")
    if username:
        u = json.loads(username)
    keywords = request.GET.get("keywords")
    page_num = request.GET.get("page_num",1)
    if keywords:
        goods_list = models.Goods.objects.filter(goods_name__contains=keywords)
    else:
        goods_list = models.Goods.objects.all()
    paginator = Paginator(goods_list,3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request,"store/goods_list.html",locals())


















def blank(request):
    return render(request, "store/base.html", locals())
