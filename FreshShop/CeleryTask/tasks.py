from __future__ import absolute_import
from FreshShop.celery import app #安装成功celery框架之后，django新生成模块

@app.task   #taskExample转换为一个任务
def taskExample():
    print("send email ok!")


@app.task
def add(x=1,y=2):
    return x+y

