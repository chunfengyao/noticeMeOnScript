#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: ycf
'''''
通过接收自定义的脚本参数，自动发送邮件
'''

import libs.sendEmail as mail
import configs.serverConfgSets as servers
import configs.senders as senders
import sys,os
import getopt

if __name__ == '__main__':
    # print('脚本：' + sys.argv[0] + '已被调用')

    commandLineAgrsHelp:str = '\n\r  -t --to      # Someone who you want to mail to.'\
                  + '\n\r  -m --msg     # The mail content.'\
                  + '\n\r  -f --file    # The file which you want to attach to the mail.'\
                  + '\n\r  -s --sub     # The subject of this mail.'\
                  + '\n\r  -h --help    # Show this page and exit.'\


    #发件人 以及发件服务器登录信息
    sender = senders.mail189_my
    #发件服务器配置
    server:servers.__ServerConfig = servers.mail189
    SMTPserver:str = server.smtp_host
    SMTPserverPort:int = server.smtp_ssl_port

    #设置默认值
    reciverAddrs:list = [sender.addr]
    reciverAddrByArgs:list = []
    context:str = '您设置的脚本提醒邮件已发出，请注意查收。'
    # 邮件主题默认值
    subject:str = '邮件提醒，来自脚本调用！！！'
    #附件列表
    fileList:list = []

    options:list = []
    #获取调用时传进来的参数列表
    try:
        options, args = getopt.getopt(sys.argv[1:], "ht:m:f:s:", ["help", "to=", "msg=", "fils=", "sub="])
    except getopt.GetoptError as err:
        # 输入的参数有误
        print('Unkown Argument! ' + err.msg + '!' +
              '\n\rOnly accept these args.\n\r' + commandLineAgrsHelp)
        exit(-1)

    for optName,optValue in options:
        if optName in ('-t', '--to'):
            if optValue:
                tmp:str = optValue
                reciverAddrByArgs.append(tmp.replace('\'', ''))
                continue
        elif optName in ('-m', '--msg'):
            if optValue:
                context = optValue
                continue
        elif optName in ('-f', '--file'):
            if optValue:
                fileAbsPath = os.path.abspath(optValue).__str__()
                fileList.append(fileAbsPath)
                print(r'已将该文件添加至附件列表：' + fileAbsPath)
                continue
        elif optName in ('-s', '--sub'):
            if optValue:
                subject = optValue
                continue
        elif optName in ('-h', '--help'):  #帮助信息
            print('You can use these args to describe the mail you want to send.\n\r' + commandLineAgrsHelp)
            exit(0)

    # 给fileList结尾增加一个逗号(空行)
    # fileList.append('')

    #优先使用通过参数设置的收件人。
    if reciverAddrByArgs.__sizeof__() != 0:
        reciverAddrs = reciverAddrByArgs


    mail.smtpPostMail(SMTPserver
                      , SMTPserverPort
                      , username=sender.account
                      , password=sender.passWord
                      , senderName=sender.name
                      , senderAddr = sender.addr
                      , reciverAddr=reciverAddrs
                      , subject=subject
                      , context=context
                      , fileList = fileList)
					  
