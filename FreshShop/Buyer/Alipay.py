from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtIrwWMbPRG10ZdC3IHusQGV/ek1DhPAVVeJvxlFgQ/KjaY5VQXcnaV7D/QPoO3ndR158zSHnYpM8rDPMqqHTWkmJog89m56DVfK2PZYPGLsxPHdqQjXRrI54udg+UcABR4p/fPw6ameiLMC2gco/+aXICUG+wEjV/iAcfLQ3D6+Sx/pymILOvBveG+1oH0GMBEVFOvaA2ELN9DwDvgY8yrXPYSnIo2WOoyWkuAaDuVowEjVv6QWJbs+j/0ntH7GjONjDRKvm+QLiBMevhUQ0hPt44YCVufQ+rYb3XB1rLsa9+AlIds4zhmGqQgNlB8SG6WuDHxtOHzUgRO52G6oDowIDAQAB
-----END PUBLIC KEY-----"""

app_private_key_string="""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAtIrwWMbPRG10ZdC3IHusQGV/ek1DhPAVVeJvxlFgQ/KjaY5VQXcnaV7D/QPoO3ndR158zSHnYpM8rDPMqqHTWkmJog89m56DVfK2PZYPGLsxPHdqQjXRrI54udg+UcABR4p/fPw6ameiLMC2gco/+aXICUG+wEjV/iAcfLQ3D6+Sx/pymILOvBveG+1oH0GMBEVFOvaA2ELN9DwDvgY8yrXPYSnIo2WOoyWkuAaDuVowEjVv6QWJbs+j/0ntH7GjONjDRKvm+QLiBMevhUQ0hPt44YCVufQ+rYb3XB1rLsa9+AlIds4zhmGqQgNlB8SG6WuDHxtOHzUgRO52G6oDowIDAQABAoIBAGofvXXBrzX+zMvIasyaRb84qj0+y3CKG1B3oNJHJTnrl2jFtJGds7n5bWT9dfX4BT0dami+BB/qgmCKtkSaiPzqew+au9EM1RChccQzv73+0stDOl+e+RfgS1Cars8o+NePrq7OKJxBPI/n25/hPcfGThY64iBu7/LH91bKLA94XHPOr3gVgKct98YKGG98r7PkcOKo5W/XlN1hxgAqljJ4MpgmuaVTNec/Zw5w0lSRxYVxv2g2lST0SiueO/bG+lPVtUt9VTS9yLJkt70vAXbAtiQRWEXFvFlClCKBqVUn6xXnRQS2IVQCd/+SHKAvKb4WMGH9vs9c7KqkeDj+2uECgYEA54sb0hx8zknSC98RRcLP5gSwntm19IyYFbHt7AJT8KqVXmQiWdcyvTovvVhtRMf0rcjMBaY+wFTCgadgDzQ6hquscLs4eJrIzMia4u6XCTefCJelPZxIqsriWgGbn3wUuLQ5ta9SYuOxMYgac7A3YPqmZPW0bKNhmlq3/y3xgdECgYEAx5zIEGGD5MHbJIps95Zq3LuGPNE91gjSJGEs3P684Yvn0M5KOhRa4alb4b07m3ovMhUNELHVjJlBGabgvtv0kahYijedkk5I4RnSgDh0CokRlEE4ou3G467ejZjGjMR6DTNeKDvlfVP9THzWkSQ5Tcvy2tfDNNYDMmYMa44ldzMCgYEApduGvTY8zIQimvBZ7g/DXnAjmFY5OYjwdDH1TObJ/A4lWuz9kj9NkDC6+7X455kYEthQFQfl0V2lyrv7Wki+V7NnnYTuya2Ogup70Gy58hdOqxf9fKmTgAw+odye/loiecBXymZg7IdPaTymPhKPSL+jK5S5fkx2YNv1Cyx839ECgYBmyVnP7ZbwLc69gzZXS7JdVYbrPEfeNg6Xwx5J8jaq4dMOF5vrSl3+A6qXlEzkY8d3v5VJunkffC8kmWTzgunuM0Tcb4UJOJyYpSZa9jby0eAmemtCorQevAZH3ZqoE+hRcdkTWLx0i9JMF6CZfpCveczlWeNgCq/8vMW6gKjUNwKBgQDJZf/YsUCUNRPiLHdByGWUHyTEdET63dtm44k5enwDDMjxmoBhiDma/+PAI/HLVSLdSz6GZg/8rDdkjRfg1HQaGgtQaE9XmZpspo6WB6kgwJtKVUIDdGW5ESUeSPL3GyT4XTYpR2tIsVx803+ZZ5UhOQl2zVxhLbUS02OJt3btgg==
-----END RSA PRIVATE KEY-----"""


alipay = AliPay(
    appid = "2016101000652524",
    app_notify_url=None,
    app_private_key_string =app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type= "RSA2"
)


####测试订单
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="874371939818",#订单号
    total_amount=str(19999),#支付金额
    subject="生鲜交易",#交易主题
    return_url=None,
    notify_url=None
)
print("https://openapi.alipaydev.com/gateway.do?"+order_string)