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
import os

mailConfig = {'sendName': '', 'sendMail': '', 'sendPass': '', 'receiverName': '', 'receiverMail': '', 'mailTitle': '', 'SMTPserver': '', 'SMTPport': ''}


# 判断文件是否存在
def tryReadConfigFile():
    if os.path.exists("config.txt") and os.path.getsize("config.txt") != 0:
        print("邮件服务已配置……")
        readConfigFile()
    else:
        writeConfigFile()
    return


# 读取配置文件
def readConfigFile():
    print("正在读取配置文件……")
    try:
        config = open("./config.txt")
        global mailConfig
        mailConfig = dict(eval(config.read(-1)))
    except PermissionError:
        print("文件读写出错，请检查文件读写权限或程序运行权限！")
        os.system("pause")
        exit()


# 写入配置文件
def writeConfigFile():
    print("开始配置邮件服务……\n")
    configSave = 'n'
    while configSave != ('y' or 'Y'):
        mailConfig['sendName'] = input("发件人昵称：")
        mailConfig['sendMail'] = input("发件人邮箱：")
        mailConfig['sendPass'] = input("发件人邮箱密码(请勿使用邮箱根密码)：")
        mailConfig['receiverName'] = input("收件人昵称：")
        mailConfig['receiverMail'] = input("收件人邮箱：")
        mailConfig['mailTitle'] = input("邮件标题：")
        mailConfig['SMTPserver'] = input("发件SMTP服务器：")
        mailConfig['SMTPport'] = input("发件SMTP服务器端口：")
        configSave = input("是否保存？(y/n)")
        print("更新配置中……")
        # print(str(mailConfig))
        config = open("config.txt", "w")
        config.write(str(mailConfig))
        print("配置更新完成！")


# 获取计算机系统启动时间
def getSystemStartTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))


# 获取当前时间
def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


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
        msg['From'] = formataddr((mailConfig['sendName'], mailConfig['sendMail'])) # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr((mailConfig['receiverName'], mailConfig['receiverMail']))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = mailConfig['mailTitle']  # 邮件的主题，也可以说是标题

        # smtp = smtplib.SMTP()
        # smtp.connect(mailConfig['SMTPserver'])
        # smtp.login(mailConfig['sendMail'], mailConfig['sendPass'])
        # smtp.sendmail(mailConfig['sendMail'], [mailConfig['receiverMail']], msg.as_string())
        # smtp.close()
        # print (mailConfig['SMTPport'])
        server = smtplib.SMTP_SSL(str(mailConfig['SMTPserver']), mailConfig['SMTPport'])  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(mailConfig['sendMail'], mailConfig['sendPass'])  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(mailConfig['sendMail'], [mailConfig['receiverMail']],
                        msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
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
    startTime = getSystemStartTime()
    tryReadConfigFile()
    pubIp, status = getPublicIp()
    localIp = getLocalIp()
    if status == 1:
        Info = "当前时间：" + nowTime + ";\n系统启动时间：" + startTime + ";\n当前公网IP：" + pubIp + "\n局域网IP：" + localIp
    else:
        Info = "当前时间：" + nowTime + ";\n系统启动时间：" + startTime + ";\n" + pubIp + ";\n局域网IP：" + localIp
    print(Info)
    sendMail(Info)
    print("10秒后自动退出")
    time.sleep(10)
