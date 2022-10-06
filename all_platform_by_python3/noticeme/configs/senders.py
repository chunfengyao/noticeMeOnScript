# -*- coding: utf-8 -*-
# author: ycf
'''''
常用的一些smtp服务器配置
'''

class _ServerConfig(object):
    smtp_host:str = ''
    smtp_ssl_port:int = 465
    smtp_port:int = 25
    imap_host:str = ''
    imap_ssl_port:int = 993
    imap_port:int = 0
    def __init__(self, smtp_host:str, smtp_ssl_port:int, smtp_port:int, imap_host:str, imap_ssl_port:int, imap_port:int) :
        super().__init__()
        self.smtp_host = smtp_host
        self.smtp_ssl_port = smtp_ssl_port
        self.smtp_port = smtp_port
        self.imap_host = imap_host
        self.imap_ssl_port = imap_ssl_port
        self.imap_port = imap_port

class _ServerConfigSet:
    _mail189:_ServerConfig = _ServerConfig(
        smtp_host='smtp.189.cn'
        , smtp_ssl_port=465
        , smtp_port=25
        , imap_host='imap.189.cn'
        , imap_ssl_port=993
        , imap_port=0
    )
    _mailgoogle:_ServerConfig = _ServerConfig(
        smtp_host='smtp.gmail.com'
        , smtp_ssl_port=465
        , smtp_port=25
        , imap_host='imap.gmail.com'
        , imap_ssl_port=993
        , imap_port=0
    )
    _mailoutlook:_ServerConfig = _ServerConfig(
        smtp_host = 'smtp.office365.com'
        , smtp_ssl_port = 587
        , smtp_port = 25
        , imap_host = 'outlook.office365.com'
        , imap_ssl_port = 993
        , imap_port = 0
    )

'''''
常用的几个用户
'''
class _sender(object):
    passWord:str=''
    addr:str=''
    account:str=addr
    name:str=''
    server:_ServerConfig=None
    serverOnSSL:bool=True
    def __init__(self, passWord:str, addr:str, name:str, server: _ServerConfig, serverOnSSL:bool):
        super().__init__()
        self.passWord=passWord
        self.addr=addr
        self.account=self.addr
        self.name=name
        self.server=server
        self.serverOnSSL=serverOnSSL

mailoutlook_someone:_sender = _sender(
    server = _ServerConfigSet._mailoutlook
    , passWord= '$your_password' #注意，有些邮箱需要生成应用密码。
    , addr = '$your_outlook_mail_address'
    , name = '$your_name'
    , serverOnSSL=False
)

