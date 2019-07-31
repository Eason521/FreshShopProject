from django.db import models

# Create your models here.

class Buyer(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户姓名")
    password = models.CharField(max_length=32,verbose_name="用户密码")
    phone = models.CharField(max_length=32,verbose_name="用户电话",blank=True,null=True)
    connect_address = models.TextField(max_length=32,verbose_name="用户地址",blank=True,null=True)
    email = models.EmailField(max_length=32, verbose_name="用户邮箱")

class Address(models.Model):
    address = models.TextField(max_length=32, verbose_name="收件地址")
    recver = models.CharField(max_length=32, verbose_name="收件人名称")
    recver_phone = models.CharField(max_length=32, verbose_name="收件人电话")
    post_number = models.CharField(max_length=32, verbose_name="收件人邮编")
    buyer_id = models.ForeignKey(to=Buyer, on_delete=models.CASCADE, verbose_name="用户id")


class Order(models.Model):
    """订单列表页"""
    order_id = models.CharField(max_length=32,verbose_name="订单编号")
    goods_count = models.IntegerField(verbose_name="订单商品数量")
    order_user = models.ForeignKey(to=Buyer,on_delete=models.CASCADE, verbose_name="订单用户")
    order_address = models.ForeignKey(to=Address,on_delete=models.CASCADE,blank=True,null=True, verbose_name="订单地址")
    order_price = models.FloatField(verbose_name="订单总价")
    order_status = models.IntegerField(default=1,verbose_name="订单状态")
    # 1代表未付款  2表示已付款未发货  3表示已发货

class OrderDetail(models.Model):
    """订单详情"""
    order_id = models.ForeignKey(to=Order,on_delete=models.CASCADE,verbose_name="订单id")
    goods_id = models.IntegerField(verbose_name="商品id")
    goods_store = models.CharField(max_length=32, verbose_name="商品店铺")
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品单价")
    goods_number = models.IntegerField(verbose_name="商品购买数量")
    goods_total = models.FloatField(verbose_name="商品总价")
    goods_image = models.ImageField(verbose_name="商品详情")


class Cart(models.Model):
    """购物车"""
    user_id = models.ForeignKey(to=Buyer,on_delete=models.CASCADE ,verbose_name="用户id")
    store_name = models.CharField(max_length=32,verbose_name="店铺名称")

    goods_id = models.IntegerField(verbose_name="商品id")
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_num = models.IntegerField(verbose_name="商品数量")
    goods_image = models.ImageField(verbose_name="商品图片")
    total = models.FloatField(verbose_name="总价")

class Area(models.Model):
    atitle = models.CharField(max_length=32,verbose_name="名称")
    aparent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)






