"""
邮件发送
"""

import smtplib #登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText #负责构建邮件格式

subject = "标题"  #标题
content = "内容"  #内容
sender = "@163.com"  #发送者
recver = """@qq.com"""  #接收者

password = ""  #授权码

message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.163.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()
