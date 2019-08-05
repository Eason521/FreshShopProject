import json
import random
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *
from Store.views import setPassword


# Create your views here.
def loginValid(fun):  # 装饰器
    def inner(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:  # 用户名称cookie
            juser = json.loads(c_user)
            user = Buyer.objects.filter(username=juser).first()
            if user:  # 用户存在
                response = fun(request, *args, **kwargs)
                return response
        return HttpResponseRedirect("/buyer/login/")
    return inner


def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        cpassword = request.POST.get("cpwd")
        email = request.POST.get("email")
        if username and password == cpassword:
            user = Buyer()
            user.username = username
            user.password = setPassword(password)
            user.email = email
            user.save()
            return HttpResponseRedirect("/buyer/login/")
    return render(request, "buyer/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        # hex_password = setPassword(password)
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            if user:
                u = json.dumps(username)
                response = HttpResponseRedirect("/buyer/index/")
                response.set_cookie("username", u)
                response.set_cookie("user_id", user.id)
                request.session["username"] = u
                return response
    return render(request, "buyer/login.html")


# @loginValid
def index(request):
    result_list = []  # 定义一个存放结果的容器
    goods_type_list = GoodsType.objects.all()
    for goods_type in goods_type_list:
        goods_list = goods_type.goods_set.filter(goods_status=1).values()[:4]
        if goods_list:
            goodsType = {
                "id": goods_type.id,
                "name": goods_type.name,
                "description": goods_type.description,
                "picture": goods_type.picture,
                "goods_list": goods_list,
            }  # 重构输出结果
            result_list.append(goodsType)
    return render(request, "buyer/index.html", locals())


def logout(request):
    response = HttpResponseRedirect("/buyer/login/")
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response


@loginValid
def goods_list(request, ):  # 前台列表页
    goodsList = []
    type_id = request.GET.get("id")
    goods_type = GoodsType.objects.filter(id=type_id).first()
    if goods_type:
        goodsList = goods_type.goods_set.filter(goods_status=1)
    return render(request, "buyer/goods_list.html", locals())


@loginValid
def goods_detail(request):  # 商品详情页
    user_id = request.COOKIES.get("user_id")
    goods_id = request.GET.get("id")  # 商品id
    if goods_id:
        goods = Goods.objects.filter(id=goods_id).first()  # 查找雏该商品信息
        if goods:
            goods_type = GoodsType.objects.filter(id=goods.goods_type_id).first()  # 查找该商品类型名称
            return render(request, "buyer/goods_details.html", locals())
    else:
        return HttpResponse("没有您查找的商品")


@loginValid
def place_order(request):  # 下订单购买

    """商品订单信息"""
    str_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    order_id = str(random.sample(range(1, 1000), 1)) + str_time  # 随机一个订单号

    goods_name = request.GET.get("goods_name")  # 商品名称
    goods = Goods.objects.filter(goods_name=goods_name).first()  # 商品对象
    goods_price = request.GET.get("goods_price")  # 商品价格
    goods_num = request.GET.get("goods_num")  # 商品数量
    total = request.GET.get("total")  # 总价
    goods_image = goods.goods_image  # 商品图片

    """获取店铺"""
    goods_store = goods.store_id.all().first()

    order_address = request.GET.get("order_address")  # 收货地址

    """获取用户信息"""
    j_username = request.COOKIES.get("username")
    username = json.loads(j_username)
    user = Buyer.objects.filter(username=username).first()

    """实例化订单对象"""
    order = Order()  # 订单页管理
    order.order_id = order_id
    order.goods_count = goods_num
    order.order_user = user
    order.order_address = order_address
    order.order_price = total
    order.order_status = 1
    order.save()

    """实例化订单详情对象"""
    order_detail = OrderDetail()  # 订单详情
    order_detail.order_id_id = order.id
    order_detail.goods_id = goods.id
    order_detail.goods_store = goods_store.store_name  # 查询店铺
    order_detail.goods_name = goods_name
    order_detail.goods_price = goods_price
    order_detail.goods_number = goods_num
    order_detail.goods_total = total
    order_detail.goods_image = goods_image
    order_detail.save()
    return render(request, "buyer/place_order.html", locals())





@loginValid
def add_cart(request):  # 加入购物车
    j_username = request.COOKIES.get("username")
    username = json.loads(j_username)

    goods_name = request.GET.get("goods_name")
    goods_num = request.GET.get("goods_num")

    user = Buyer.objects.filter(username=username).first()
    goods = Goods.objects.filter(goods_name=goods_name).first()  # 商品对象
    store_name = goods.store_id.all().first()  # 店铺对象

    goods_price = goods.goods_price

    total = int(goods_num) * goods_price

    cart = Cart()
    cart.user_id = user
    cart.store_name = store_name.store_name
    cart.goods_id = goods.id
    cart.goods_name = goods_name
    cart.goods_price = goods_price
    cart.goods_num = goods_num
    cart.total = total
    cart.goods_image = goods.goods_image
    cart.save()
    return render(request, "buyer/goods_details.html", locals())


@loginValid
def cart(request):  # 查看购物车
    user_id = request.COOKIES.get("user_id")
    goods_list = Cart.objects.filter(user_id_id=user_id)
    num = len(goods_list)
    goods_total = sum([int(i.total) for i in goods_list])
    return render(request, "buyer/cart.html", locals())

@loginValid
def del_cart_goods(request):
    id = request.GET.get("id")  #获取删除的商品id
    Cart.objects.filter(id=id).first().delete()
    return HttpResponseRedirect("/buyer/cart/")




def cart_order(request):
    """购物车商品订单信息"""
    str_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    order_id = str(random.sample(range(1, 1000), 1)) + str_time  # 随机一个订单号

    """获取用户信息"""
    j_username = request.COOKIES.get("username")
    username = json.loads(j_username)
    user = Buyer.objects.filter(username=username).first()

    if request.method == "POST":
        post_data = request.POST  # 获取所有post提交过来的数据
        cart_data = []  # 收集前端传递过来的商品
        for k, v in post_data.items():
            if k.startswith("goods_"):
                cart_data.append(Cart.objects.get(id=int(v)))

        goods_count = len(cart_data)  # 商品数量
        goods_total = sum([int(i.total) for i in cart_data])  # 订单的总价

        """实例化订单对象"""
        order = Order()  # 订单页管理
        order.order_id = order_id
        order.goods_count = goods_count
        order.order_user = user
        # order.order_address = order_address
        order.order_price = goods_total
        order.order_status = 1
        order.save()

        """实例化订单详情对象"""
        for detail in cart_data:
            order_detail = OrderDetail()  # 订单详情
            order_detail.order_id = order
            order_detail.goods_id = detail.goods_id
            order_detail.goods_store = detail.store_name  # 查询店铺
            order_detail.goods_name = detail.goods_name
            order_detail.goods_price = detail.goods_price
            order_detail.goods_number = detail.goods_num
            order_detail.goods_total = detail.total
            order_detail.goods_image = detail.goods_image
            order_detail.save()
        url = "/buyer/pay_order/?order_id=%s&goods_price=%s"%(order.order_id,goods_total)
        return HttpResponseRedirect(url)
    else:
        cart = Cart.objects.values()
        return render(request, "buyer/place_order.html", locals())

@loginValid
def user_center_order(request):
    user_id = request.COOKIES.get("user_id")
    #已付款订单列表
    #未付款订单列表
    times = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    orders = Order.objects.filter(order_user_id=user_id) #获取该用户的订单
    for sta in orders:
        if sta.order_status == 1: #未付款状态
            order_detail1 = OrderDetail.objects.filter(order_id__order_status=1,order_id_id=sta.id)
        elif sta.order_status == 2: #未发货
            order_detail2 = OrderDetail.objects.filter(order_id__order_status=2,order_id_id=sta.id)
    return render(request,"buyer/user_center_order.html",locals())

def user_center_info(request):
    user_id = request.COOKIES.get("user_id")
    user = Buyer.objects.filter(id=user_id).first()

    return render(request,"buyer/user_center_info.html",locals())

@loginValid
def user_center_site(request):
    """添加地址"""
    # address = Address()  # 保存地址
    # address = address
    # recver = receiver
    # recver_phone = receiver_phone
    # post_number = post_number
    # buyer_id = user
    return render(request, "buyer/user_center_site.html", locals())

# 获取省份信息
def getProvince(request):
    provinces = Area.objects.filter(aparent__isnull=True)
    res = []
    for i in provinces:
        res.append([i.id, i.atitle])
    return JsonResponse({"provinces":res})
# 获取市信息
def getCity(request):
    city_id = request.GET.get('city_id')
    cities = Area.objects.filter(aparent_id=city_id)
    res = []
    for i in cities:
        res.append([i.id, i.atitle])
    return JsonResponse({"cities":res})
# 获取县信息
def getDistrict(request):
    district_id = request.GET.get('district_id')
    cities = Area.objects.filter(aparent_id=district_id)
    res = []
    for i in cities:
        res.append([i.id, i.atitle])
    return JsonResponse({'district': res})


















from alipay import AliPay

"""支付模块"""


@loginValid
def pay_order(request):
    goods_price = request.GET.get("goods_price")  # 获取订单金额
    order_id = request.GET.get("order_id")  # 获取订单号
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtIrwWMbPRG10ZdC3IHusQGV/ek1DhPAVVeJvxlFgQ/KjaY5VQXcnaV7D/QPoO3ndR158zSHnYpM8rDPMqqHTWkmJog89m56DVfK2PZYPGLsxPHdqQjXRrI54udg+UcABR4p/fPw6ameiLMC2gco/+aXICUG+wEjV/iAcfLQ3D6+Sx/pymILOvBveG+1oH0GMBEVFOvaA2ELN9DwDvgY8yrXPYSnIo2WOoyWkuAaDuVowEjVv6QWJbs+j/0ntH7GjONjDRKvm+QLiBMevhUQ0hPt44YCVufQ+rYb3XB1rLsa9+AlIds4zhmGqQgNlB8SG6WuDHxtOHzUgRO52G6oDowIDAQAB
-----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAtIrwWMbPRG10ZdC3IHusQGV/ek1DhPAVVeJvxlFgQ/KjaY5VQXcnaV7D/QPoO3ndR158zSHnYpM8rDPMqqHTWkmJog89m56DVfK2PZYPGLsxPHdqQjXRrI54udg+UcABR4p/fPw6ameiLMC2gco/+aXICUG+wEjV/iAcfLQ3D6+Sx/pymILOvBveG+1oH0GMBEVFOvaA2ELN9DwDvgY8yrXPYSnIo2WOoyWkuAaDuVowEjVv6QWJbs+j/0ntH7GjONjDRKvm+QLiBMevhUQ0hPt44YCVufQ+rYb3XB1rLsa9+AlIds4zhmGqQgNlB8SG6WuDHxtOHzUgRO52G6oDowIDAQABAoIBAGofvXXBrzX+zMvIasyaRb84qj0+y3CKG1B3oNJHJTnrl2jFtJGds7n5bWT9dfX4BT0dami+BB/qgmCKtkSaiPzqew+au9EM1RChccQzv73+0stDOl+e+RfgS1Cars8o+NePrq7OKJxBPI/n25/hPcfGThY64iBu7/LH91bKLA94XHPOr3gVgKct98YKGG98r7PkcOKo5W/XlN1hxgAqljJ4MpgmuaVTNec/Zw5w0lSRxYVxv2g2lST0SiueO/bG+lPVtUt9VTS9yLJkt70vAXbAtiQRWEXFvFlClCKBqVUn6xXnRQS2IVQCd/+SHKAvKb4WMGH9vs9c7KqkeDj+2uECgYEA54sb0hx8zknSC98RRcLP5gSwntm19IyYFbHt7AJT8KqVXmQiWdcyvTovvVhtRMf0rcjMBaY+wFTCgadgDzQ6hquscLs4eJrIzMia4u6XCTefCJelPZxIqsriWgGbn3wUuLQ5ta9SYuOxMYgac7A3YPqmZPW0bKNhmlq3/y3xgdECgYEAx5zIEGGD5MHbJIps95Zq3LuGPNE91gjSJGEs3P684Yvn0M5KOhRa4alb4b07m3ovMhUNELHVjJlBGabgvtv0kahYijedkk5I4RnSgDh0CokRlEE4ou3G467ejZjGjMR6DTNeKDvlfVP9THzWkSQ5Tcvy2tfDNNYDMmYMa44ldzMCgYEApduGvTY8zIQimvBZ7g/DXnAjmFY5OYjwdDH1TObJ/A4lWuz9kj9NkDC6+7X455kYEthQFQfl0V2lyrv7Wki+V7NnnYTuya2Ogup70Gy58hdOqxf9fKmTgAw+odye/loiecBXymZg7IdPaTymPhKPSL+jK5S5fkx2YNv1Cyx839ECgYBmyVnP7ZbwLc69gzZXS7JdVYbrPEfeNg6Xwx5J8jaq4dMOF5vrSl3+A6qXlEzkY8d3v5VJunkffC8kmWTzgunuM0Tcb4UJOJyYpSZa9jby0eAmemtCorQevAZH3ZqoE+hRcdkTWLx0i9JMF6CZfpCveczlWeNgCq/8vMW6gKjUNwKBgQDJZf/YsUCUNRPiLHdByGWUHyTEdET63dtm44k5enwDDMjxmoBhiDma/+PAI/HLVSLdSz6GZg/8rDdkjRfg1HQaGgtQaE9XmZpspo6WB6kgwJtKVUIDdGW5ESUeSPL3GyT4XTYpR2tIsVx803+ZZ5UhOQl2zVxhLbUS02OJt3btgg==
-----END RSA PRIVATE KEY-----"""
    alipay = AliPay(
        appid="2016101000652524",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(goods_price),  # 支付金额
        subject="普通商品",  # 交易主题
        return_url="http://127.0.0.1:8000/buyer/pay_result/",  # 支付完成要跳转的本地路由,
        notify_url="http://127.0.0.1:8000/buyer/pay_result/",  # 支付完成要跳转的本地异步路由
    )

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)


@loginValid
def pay_result(request):
    order_id = request.GET.get("out_trade_no")
    order = Order.objects.filter(order_id=order_id).first()
    order.order_status = 2
    order.save()
    """
    支付宝支付成功自动用get请求返回的参数
    #编码
    charset=utf-8
    #订单号
    out_trade_no=10002
    #订单类型
    method=alipay.trade.page.pay.return
    #订单金额
    total_amount=1000.00
    #校验值
    sign=enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D&trade_no=2019072622001422161000050134&auth_app_id=2016093000628355&version=1.0&app_id=2016093000628355
    #订单号
    trade_no=2019072622001422161000050134
    #用户的应用id
    auth_app_id=2016093000628355
    #版本
    version=1.0
    #商家的应用id
    app_id=2016093000628355
    #加密方式
    sign_type=RSA2
    #商家id
    seller_id=2088102177891440
    #时间
    timestamp=2019-07-26
    """
    return render(request, "buyer/pay_result.html", locals())


def base(request):
    return render(request, "buyer/base.html",locals())
