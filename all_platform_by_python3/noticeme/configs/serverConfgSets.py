# -*- coding: utf-8 -*-
# author: ycf
'''''
常用的一些smtp服务器配置
'''

class __ServerConfig(object):
    smtp_host:str = ''
    smtp_ssl_port:int = 465
    smtp_port:int = 25
    imap_host:str = ''
    imap_ssl_port:int = 0
    imap_port:int = 0
class mail189(__ServerConfig):
    smtp_host = 'smtp.189.cn'
    smtp_ssl_port = 465
    smtp_port = 25
    imap_host = 'imap.189.cn'
    imap_ssl_port = 0
    imap_port = 0
