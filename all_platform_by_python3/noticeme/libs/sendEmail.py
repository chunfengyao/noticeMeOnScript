#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: ycf
'''''
使用smtplib发送邮件 smtp服务的tls模式
'''

import smtplib
import imaplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email.errors
import email.header as Header
from email.utils import parseaddr, formataddr
from email import encoders


def _format_addr(s:str):
    name, addr = parseaddr(s)
    return formataddr(
        (Header.Header(name, 'utf-8').encode(),
        addr if isinstance(addr, str) else addr)
    ) #仅仅P    ython3中生效，Python3默认的str就是unicode


def smtpPostMail(SMTPserver:str = ''
                 , SMTPserverPort:int = ''
                 , username:str = ''
                 , password:str = ''
                 , senderName:str = ''
                 , senderAddr:str = ''
                 , reciverAddr:list = [str]
                 , subject:str ='', context:str ='', fileList:list = [str]):

    # 连接并登陆登录
    # mailserver = smtplib.SMTP(SMTPserver, 25)
    # ssl的端口号默认是465
    mailserver = smtplib.SMTP_SSL(host=SMTPserver, port=SMTPserverPort)
    # 调试等级
    # mailserver.set_debuglevel(1)
    mailserver.login(username, password)


    # 取出所有的接收者
    recivers:str = u''
    for reciver in reciverAddr:
        if reciver:
            recivers += u'%s <%s>' % (reciver,reciver)  #拼接到一起

    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>'% (senderName,senderAddr))
    msg['To'] = _format_addr(recivers)
    msg['Subject'] = Header.Header(u'%s'% subject, 'utf-8').encode()
    msg['Content-Type'] = "text/html; charset=utf-8"
    msg['Content-Transfer-Encoding'] = "quoted-printable"
    #文本段
    msg.attach(MIMEText(context))

    attachListDesc = ''

    #所有文件的文件列表（发送后，接收端无目录结构，建议添加参数，可选将目录压缩后发送）
    allFilesList:list = listAllFileFromPathSet(fileList)
    # 文件段（文件夹处理后生成的文件列表）
    for filePath in allFilesList:
        if os.path.exists(filePath) and os.path.isfile(filePath):
            file = open(filePath, 'rb')
            fileDataToEmail = MIMEApplication(file.read())
            fileDataToEmail.add_header('Content-Disposition', 'attachment', filename=file.name)
            msg.attach(fileDataToEmail)
            attachListDesc += filePath
        # print('已添加附件：%s' %(filePath))

    print('\n\r #The mail to send seems like：')
    print(' ##From：' + u'%s <%s>'% (senderName, senderAddr))
    print(' ##To：' + recivers)
    print(' ##Subject：' + subject)
    print(' ##Context：' + context)
    print(' ##AttachList：' + attachListDesc)

    # 开始发送(sender、reciver不可为中文！)
    mailserver.sendmail(from_addr=senderAddr, to_addrs=reciverAddr, msg=msg.as_string())
    # mailserver.send_message(msg=msg, from_addr=senderAddr, to_addrs=reciverAddr)
    # mailserver.sendmail(from_addr='', to_addrs=reciver, msg=msg.__str__().encode("utf-8"))
    mailserver.quit()
    print('\n\r #Mail with subject：%s \n\rSended Sucessful !' % (subject))


def listAllFileFromPathSet(path:list = [str]):
    allFilesList = []
    # 文件夹处理（生成文件列表）
    for filePath in path:
        # 如果是目录的话，递归遍历目录
        if os.path.exists(filePath) and os.path.isdir(filePath):
            for rootDirPath, dirs, files in os.walk(filePath):
                # for i in dirs:
                #     print(os.path.abspath(root)+'/'+i)
                for file in files:
                    allFilesList.append(os.path.abspath(rootDirPath) + '/' + file)
        # 如果是文件的话，直接附加上去
        elif os.path.exists(filePath) and os.path.isfile(filePath):
            allFilesList.append(filePath)
    return allFilesList