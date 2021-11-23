#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
import socket
import time
import urllib.error
import urllib.request
from email.mime.text import MIMEText
from email.utils import formataddr
import psutil


#获取计算机系统启动时间
def getSystemStartTime():
    startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
    return startTime


# 获取当前时间
def getTime():
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return nowTime


# 获取内网IP
def getLocalIp():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        ip = addr
    except Exception as e:
        ip = "get local ip failure! Code:", e
    return ip


# 获取外网IP
def getPublicIp():
    readStatus = 0
    ip = ""
    try:
        url = "http://pv.sohu.com/cityjson"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/84.0.4147.105 Safari/537.36 "
        }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        # print(response.read())
        html = response.read().decode("gbk")
        # print(html)
        location = str(html).split(', "cname": "', 1)[1]
        location = location.split('"}', 1)[0]
        ip = str(html).split('"cip": "', 1)[1]
        ip = ip.split('", "cid": "', 1)[0] + "\n位置：" + location
        readStatus = 1
    except Exception as e:
        ip = "公网IP获取失败! Code:" + str(e)
    return ip, readStatus


# 发送邮件功能
def sendMail(valueIndex):
    ret = True
    try:
        msg = MIMEText(valueIndex, 'plain', 'utf-8')
        msg['From'] = formataddr(["NUC服务器", "2407174040@qq.com"])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["user", "994000103@qq.com"])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "NUC服务器已启动"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login("2407174040@qq.com", "ehzxgjoyrlrgdjbb")  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail("2407174040@qq.com", ["994000103@qq.com"], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e1:
        ret = False
        print("错误:", e1)
    finally:
        if ret:
            print("邮件发送成功")
        else:
            print("邮件发送失败")


if __name__ == "__main__":
    nowTime = getTime()
    pubIp, status = getPublicIp()
    localIp = getLocalIp()
    startTime = getSystemStartTime()
    if status == 1:
        Info = "当前时间：" + nowTime + ";\n系统启动时间：" + startTime + ";\n当前公网IP：" + pubIp + "\n局域网IP：" + localIp
    else:
        Info = "当前时间：" + nowTime + ";\n系统启动时间：" + startTime + ";\n" + pubIp + ";\n局域网IP：" + localIp
    print(Info)
    sendMail(Info)
