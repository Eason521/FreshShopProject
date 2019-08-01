"""
邮件发送
"""

import smtplib #登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText #负责构建邮件格式

subject = "博客"  #标题
content = "https://blog.csdn.net/qq_40576301"  #内容
sender = "1946648105@163.com"  #发送者
recver = """3392279511@qq.com,1403617606@qq.com"""  #接收者

password = ""  #授权码

message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.163.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()
