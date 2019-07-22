#coding:utf-8
import hashlib
import json

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from Store import models


# Create your views here.
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
                    # request.session["username"] = username
                    return response
    return response

def index(request):
    username = request.COOKIES.get("username")
    if username:
        return render(request, "store/index.html",locals())
    return HttpResponseRedirect("/store/login/")

def blank(request):
    return render(request,"store/blank.html",locals())
