from __future__ import absolute_import
import json

import requests

from FreshShop.celery import app  # 安装成功celery框架之后，django新生成模块


@app.task   #taskExample转换为一个任务
def taskExample():
    print("send email ok!")


@app.task
def add(x=1,y=2):
    return x+y

@app.task
def dingTalk():
    """钉钉机器人"""
    url=""  #钉钉机器人地址

    headers = {
        "Content-Type":"application/json",
        "chartset":"utf8"

    }

    requests_data = {
        "msgtype":"text",
        "text":{
            "content":""
        },
        "at":{
            "atMobiles":[],
        },
        "isAtAll":True
    }

    sendData = json.dumps(requests_data)
    response = requests.post(url,headers=headers,data=sendData)
    content =response.json()
    print(content)



