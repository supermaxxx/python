#!D:\Python27\pythonw.exe
# -*- coding: utf-8 -*-
import urllib, urllib2
import json
import sys, os, re, time
import socket
import smtplib
import email
from email.header import decode_header
from PyWapFetion import Fetion

##part1 发送飞信
def send_sms(fx_info, context):
    try:
        myfetion = Fetion(fx_info['user'], fx_info['password'])
        myfetion.send(fx_info['user'], context, sm=True)
        myfetion.logout()
        return 1
    except:
        return 0

##part2 获取外网ip
class getIp(object):
    def getIp(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except:
            try:
                myip = self.visit("http://www.bliao.com/ip.phtml")
            except:
                try:
                    myip = self.visit("http://www.whereismyip.com/")
                except:
                    myip = "127.0.0.1"
        return myip
    def visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)	

##part3 查找ip的地域信息
class getIpInfo(object):
    def __init__(self):
        self.url = "http://ip.taobao.com/service/getIpInfo.php?ip="
        self.re_ipaddress = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        self.re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
    def ip_location(self,ip):
        data = urllib.urlopen(self.url + ip).read()
        datadict=json.loads(data)
        for oneinfo in datadict:
            if "code" == oneinfo:
                if datadict[oneinfo] == 0:
                    return datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]
    def getIpInfo(self,input):
        if self.re_ipaddress.match(input):
            city_address = self.ip_location(input)
        elif (self.re_domain.match(input)):
            result = socket.getaddrinfo(input.strip(), None)
            ipaddr = result[0][4][0]
            city_address = self.ip_location(ipaddr)
        return city_address

##part4 接收邮件
def accp_mail_pop3(mail_info):
    import poplib
    try:
        p = poplib.POP3(mail_info['server'])
        p.user(mail_info['user'])
        p.pass_(mail_info['password'])
        ret = p.stat()
    except poplib.error_proto,e:
#        print "Login failed:",e
        return 0
        sys.exit(1)
    item = p.list()[1][-1]
    number,octets = item.split(' ')
    lines = p.retr(number)[1]
    msg = email.message_from_string("\n".join(lines))
    return msg

def accp_mail_imap(mail_info):
    import imaplib
    try:
        m = imaplib.IMAP4(mail_info['server'])
        m.login(mail_info['user'], mail_info['password'])
    except:
        return 0
        sys.exit(1)
    result,message = m.select()
    num = message[0]
    rc,data =  m.fetch(num, '(RFC822)')
    msg = email.message_from_string(data[0][1])
    return msg

##part5 分析邮件并执行相应操作
def action(mail_info, msg):
    title = email.Header.decode_header(msg['subject'])[0][0]
    fromwho = email.Header.decode_header(msg['from'])[0][0]
 #   _fromwho = email.Header.decode_header(msg['from'])[0][0]
 #   if mail_info['server'] == 'pop.qq.com':
 #       re_fromwho = re.compile(r'<.*>')
 #       __fromwho = re_fromwho.findall(_fromwho)
 #       fromwho = __fromwho[0].replace('<','').replace('>','')
 #   else:
 #       fromwho = _fromwho
    if fromwho == '1376xxxx677@139.com':
        if title == 'shutdown':
            return 1


if __name__ == '__main__':
    localip = getIp().getIp()
    localipinfo = getIpInfo().getIpInfo(localip)
    loguser = os.popen('echo %username%').readline()
    info = 'pc is started!!!\nlogin as %s' %loguser
    sms = info + unicode(localipinfo).encode("UTF-8")

    mail_163 = {'server':'pop.163.com',
                 'user':'xxxxxx',
                 'password':'xxxxxx'}
    mail_qq = {'server':'pop.qq.com',
               'user':'xxxxxx',
               'password':'xxxxxx'}
    mail_ucloud = {'server':'mail.ucloud.cn',
                   'user':'xxxxxx',
                   'password':'xxxxxx'}
    fx_info = {'user':'1376xxxx677',
               'password':'xxxxxx'}

    #pop3: mail_qq, mail_163 / imap: mail_ucloud
    mail_target = mail_ucloud    #收件信息，需要修改

    while send_sms(fx_info, sms) == 0:
        time.sleep(5)

    while 1:
        time.sleep(10)
        if mail_target['server'] == 'mail.ucloud.cn':
            msg = accp_mail_imap(mail_target)
        elif mail_target['server'] == 'pop.163.com' or mail_target['server'] == 'pop.qq.com':
            msg = accp_mail_pop3(mail_target)
        tag = action(mail_target, msg)
#        print tag
        if tag == 1:
            os.system('shutdown -s -t 3 -c closing...hahaha~~~')
