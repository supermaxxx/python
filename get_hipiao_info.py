#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Friday, Feb 14, 2014
Updated on Thursday, May 8, 2015
@author: wangyucheng
"""

import urllib
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

class Email(object):
    def __init__(self, MAIL_ADDRESS, MAIL_SUBJECT, MAIL_MESSAGE, ATTACHMENT=None):
        self.MAIL_HOST = 'smtp.163.com'
        self.MAIL_USERNAME = '??????@163.com'
        self.MAIL_PASSWORD = '??????'
        self.MAIL_TO = MAIL_ADDRESS # address to mail
        self.MAIL_SUBJECT = MAIL_SUBJECT  # title of the mail
        self.MAIL_MESSAGE = MAIL_MESSAGE  # body of the mail
        self.ATTACHMENT = ATTACHMENT  # attachment
    def run(self):
        body = MIMEText(self.MAIL_MESSAGE)
        msg = MIMEMultipart()
        msg.attach(body)
        msg['To'] = self.MAIL_TO
        msg['from'] = self.MAIL_USERNAME
        msg['subject'] = self.MAIL_SUBJECT
        if self.ATTACHMENT != None:
            attachment = self.ATTACHMENT.split('/')[-1]
            att = MIMEText(open(self.ATTACHMENT).read(),'base64','gb2312')
            att["Content-Disposition"] = 'attachment;filename="' + attachment + '"'
            msg.attach(att)
        try:
            session = smtplib.SMTP()
            session.connect(self.MAIL_HOST)
            session.login(self.MAIL_USERNAME,self.MAIL_PASSWORD)
            session.sendmail(self.MAIL_USERNAME,self.MAIL_TO,msg.as_string())
            session.close()
            msg = 'Send Email Successfully.'
            print msg
        except Exception,e:
            print e


def report_by_email(mail_list, text):
    _now = datetime.now()
    now = _now.strftime("%Y-%m-%d %H:%M:%S")
    title = "hipiao嘉定罗宾森电影院排片表(刷新时间: %s)" %now
    if text != None:
        for mail_address in mail_list:
            Email(mail_address, title, text).run()

def cs(a):
    return a.decode('utf-8')


today = date.today()
tomorrow = today + timedelta(1)
days = [str(today),str(tomorrow)]
days = {str(today):"今日", str(tomorrow):"明日"}
url = 'http://cinema.hipiao.com/dadi_jiading'
response = urllib.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
text = ''  #邮件内容
for day,value in days.items():
    msg = cs("<大地数字影院--上海嘉定罗宾森广场--电影排片表--%s(%s)>\n\n" %(day.replace('-','/'),value))
    movieList = soup.findAll('div', attrs={'id':'planDataList'})
    if(movieList):
        lis = movieList[0].findAll('li', attrs={'day':day})
        for li in lis:
            #pm = li.find('div').text    #片名(地区)
            pm = li['film']    #片名
            ps = li.findAll('p')
            pcs = ps[3].text.split()
            _pc = pcs[2] if len(pcs)==3 else 'Unknown'    #片长
            if _pc != 'Unknown':
                try:
                    pc = int(_pc)
                    pc = str(pc) + cs('分钟')
                except Exception:
                    pc = _pc
            else:
                pc = 'Unknown'
            dy = ps[0].text.replace(' / ',',').split()[2]    #导演
            yys = ps[1].text.replace(' / ',',').split()[1].split(',')    #演员
            yy = yys[0] + ',' + yys[1] if len(yys) > 1 else yys[0]    #演员（取最多前2个）
            dq = ps[2].text.replace(' ',',').split()[2].replace(',,,,,,,,,,','')    #地区
            msg += cs('片名: ') + pm + '\n'
            msg += cs('片长: ') + pc + '\n'
            msg += cs('导演: ') + dy + '\n'
            msg += cs('演员: ') + yy + '\n'
            msg += cs('地区: ') + dq + '\n'
            cts = li.findAll('div', attrs={'class':'ciname_table'})
            for ct in cts:
                tr = ct.findAll('tr')
                msg += cs('放映时间 语种/制式 影厅 会员价/原价: \n') 
                for tds in tr:
                    td = tds.findAll('td')
                    if len(td) > 0:
                        sijian = td[0].text    #放映时间
                        yuyan = td[1].text    #语种/制式
                        yingting = td[2].text    #影厅
                        jiage =  td[4].text[1:] + cs('元/') + td[3].text[1:] + cs('元')    #会员价/原价
                        msg += sijian.split()[0] + '    ' + yuyan + ' ' + yingting + ' ' + jiage + '\n'
            msg += '\n'
    m = msg.encode('utf-8')
    text += m

print text
report_by_email(["??????@qq.com", ], text)
