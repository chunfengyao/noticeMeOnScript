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

from configs.senders import _sender


def _format_addr(s:str):
    name, addr = parseaddr(s)
    return formataddr(
        (Header.Header(name, 'utf-8').encode(),
        addr if isinstance(addr, str) else addr)
    ) #仅仅Python3中生效，Python3默认的str就是unicode

def smtpPostMail(sender:_sender
                 , reciverAddr:list = [str]
                 , subject:str ='', context:str ='', fileList:list = [str]):

    try:
        if sender.serverOnSSL:
            # ssl的端口号默认是465
            mailserver = smtplib.SMTP_SSL(host=sender.server.smtp_host, port=sender.server.smtp_ssl_port)
        else:
            # 连接并登陆登录
            mailserver = smtplib.SMTP(sender.server.smtp_host, sender.server.smtp_port)
        mailserver.timeout=10
        mailserver.ehlo()  # 发送SMTP 'ehlo' 命令
        try:
            mailserver.starttls()
        except Exception as e:
            print('StarTTLS may not supported by this server!')
            print('Here is the Exception msg:')
            print(e)
    except Exception as e:
        print('Sorry, Failed to connect the smtp server!!!')
        print('Here is the Exception msg:')
        print(e)
        #终止流程
        exit(3)
        return
    # 调试等级
    # mailserver.set_debuglevel(1)
    mailserver.login(sender.account, sender.passWord)


    # 取出所有的接收者
    recivers:str = u''
    for reciver in reciverAddr:
        if reciver:
            recivers += u'%s <%s>' % (reciver,reciver)  #拼接到一起

    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>'% (sender.name,sender.addr))
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
            safeFileName:str = file.name.split(os.path.sep)[-1]
            fileDataToEmail.add_header('Content-Disposition', 'attachment', filename=safeFileName)
            msg.attach(fileDataToEmail)
            attachListDesc += u'%s at %s'% (safeFileName, filePath)

    print('\n\r #The mail to send is：')
    print(' ##From：' + u'%s <%s>'% (sender.name, sender.addr))
    print(' ##To：' + recivers)
    print(' ##Subject：' + subject)
    print(' ##Context：' + context)
    print(' ##AttachList：' + attachListDesc)

    try:
        # 开始发送(sender、reciver不可为中文！)
        mailserver.sendmail(from_addr=sender.addr, to_addrs=reciverAddr, msg=msg.as_string())
        # mailserver.send_message(msg=msg, from_addr=senderAddr, to_addrs=reciverAddr)
        # mailserver.sendmail(from_addr='', to_addrs=reciver, msg=msg.__str__().encode("utf-8"))
    except smtplib.SMTPHeloError as e:
        print('Failed to get the hello msg from SMTP Server. Please check the SMTP settings for your mail account.')   #接收方服务器拒绝收信
        print('Here is the Exception msg:')
        print(e)
        exit(4)
    except smtplib.SMTPRecipientsRefused as e:
        print('This mail is refused by recipient\'s server.')   #接收方服务器拒绝收信
        print('Here is the Exception msg:')
        print(e)
        exit(4)
    except smtplib.SMTPSenderRefused as e:
        print('The post mail request was refused by SMTP Server. Please contract to server\'s administrator.')
        print('Here is the Exception msg:')
        print(e)
        exit(4)
    except smtplib.SMTPDataError as e:
        print('This server reply the error data. Please retry later')
        print('Here is the Exception msg:')
        print(e)
        exit(4)
    except smtplib.SMTPNotSupportedError as e:
        print('This server seems not support SMTP. Please check and retry.')
        print('Here is the Exception msg:')
        print(e)
        exit(4)
    except Exception as e:
        print('Sorry, something error! We failed to post this mail, you can retry later...')
        print('Here is the Exception msg:')
        exit(9)

    print('\n\r # Mail with subject：%s \n\rSended Sucessful !' % (subject))
    #退出服务器
    mailserver.quit()
    exit(0)

def listAllFileFromPathSet(path:list = [str]):
    allFilesList = []
    # 文件夹处理（生成文件列表）
    for filePath in path:
        # 如果是目录的话，递归遍历目录
        if os.path.exists(filePath) and os.path.isdir(filePath):
            for rootDirPath, dirs, files in os.walk(filePath):
                for file in files:
                    allFilesList.append(os.path.abspath(rootDirPath) + '/' + file)
        # 如果是文件的话，直接附加上去
        elif os.path.exists(filePath) and os.path.isfile(filePath):
            allFilesList.append(filePath)
    return allFilesList

