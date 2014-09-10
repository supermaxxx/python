#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Thursday Sep 10 17:00 2014
@author: wangyucheng
'''

import sys, os
import commands
import re
import logging
import urllib
from datetime import datetime, date
from bs4 import BeautifulSoup
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

_vvshu_list_1 = []
_vvshu_list_2 = []
_madouer_list_1 = []
_madouer_list_2 = []

class Writer():
    def __init__(self, filename):
        self.filename = filename
    def write(self, msg):
        f = file(self.filename, 'a')
        f.write(msg)
        f.close()


class Email(object):
    def __init__(self, MAIL_SUBJECT, MAIL_MESSAGE, ATTACHMENT=None):
        self.MAIL_HOST = 'smtp.163.com'
        self.MAIL_USERNAME = '******@163.com'
        self.MAIL_PASSWORD = '******'
        self.MAIL_TO = '******@qq.com'
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
            logger.info(msg)
        except Exception,e:
            print e
            logger.info(e)

def add_head(filename):
    stdout_pre = sys.stdout
    sys.stdout = Writer(filename)
    print '<html>'
    print '<head>'
    print '<meta http-equiv="Content-Language" content="zh-cn">'
    print '<meta http-equiv="Content-Type" content="text/html; charset=gb2312">'
    print '</head>'
    print '<body onload="resizeimg();">'
    print '<style> a {text-decoration: none;}</style>'
    print
    print '<script>'
    print 'var count = 10;'
    print
    print 'function zoompic(obj)'
    print '{'
    print '  var s=obj.style.zoom;'
    print '  if ((s== "undefined") || (s==""))'
    print '  {'
    print '     count=10;'
    print '  }'
    print '  else'
    print '  {'
    print '    l=s.length;'
    print '    l=l-1;'
    print '    s2=s.substr(0,l);'
    print '    count=parseInt(s2);'
    print '    count=count /10;'
    print '    // alert(count);'
    print '  }'
    print '  if (count<2) count=2;'
    print '  if (count>90) count=90;'
    print '  if (event.wheelDelta >= 120)  count++;'
    print '  else if (event.wheelDelta <= -120) count--;'
    print "  obj.style.zoom = count + '0%';"
    print '  return false;'
    print '}'
    print
    print 'function Counting(count)'
    print '{ '
    print '  if (event.wheelDelta >= 120)  count++;'
    print '  else if (event.wheelDelta <= -120) count--; '
    print '  return count; '
    print '}'
    print '</script>'
    print
    print '<script>'
    print 'function resizeimg()'
    print '{'
    print ' for (j=0;j<document.images.length;j++)'
    print ' {'
    print '  n= document.images[j].name;'
    print '  if  (n.indexOf("p")==0)'
    print ' }'
    print '}'
    print '</script>'
    sys.stdout = stdout_pre


def  task_begin(name):
    _begin_time = datetime.now()
    begin_time = _begin_time.strftime("%Y-%m-%d %H:%M:%S")
    msg = "Downloading %s...BEGIN -- Current Time: %s" %(name, begin_time)
    print msg
    logger.info(msg)
    return _begin_time


def task_end(name, _begin_time):
    _end_time = datetime.now()
    end_time = _end_time.strftime("%Y-%m-%d %H:%M:%S")
    cost = (_end_time - _begin_time).seconds
    msg = "Downloading %s...END   -- Current Time: %s" %(name, end_time)
    print msg
    logger.info(msg)
    msg = "Downloading %s...Suc, Time Cost: %ss." %(name, cost)
    print msg
    logger.info(msg)


def CheckLocal(_name, day):
    work_dir = '%s/%s/%s/' %(main_dir, day, _name)
    if os.path.exists(work_dir) == False:
        os.system("mkdir -p %s" %work_dir)
    return work_dir


class vvshu():
    def __init__(self, name):
        self.name = name
        self.main_url = 'http://www.vvshu.com/view/%s/' %self.name
    def CheckRemote(self):
        response = urllib.urlopen(self.main_url)
        html = response.read()
        soup = BeautifulSoup(html)
        NewList = soup.findAll('div', attrs={'class':'vvmlt'})
        if(NewList):
            down_month = []
            _new_baseurls = []
            lis = NewList[0].findAll('li')
            for li in lis:
                l = li.findAll('a')
                _l = li.findAll('img')
                _text = _l[0]['alt']
                text = _text.encode('utf-8').replace('<b>', '').replace('</b>', '')
                new_baseurl = l[0]['href']
                month = int(new_baseurl.split('/')[5])
                url_month = (new_baseurl, month, text)
                down_month.append(month)
                _new_baseurls.append(url_month)
            month = max(down_month)
            new_baseurls = []
            for i in _new_baseurls:
                if i[0].split('/')[5] == str(month):
                    args = [self.name, i]
                    new_baseurls.append(args)
            return new_baseurls
        else:
            return None
    def getlist(self, LIST):
        a = self.CheckRemote()
        if a and len(a) > 0: 
            LIST.append(a)

class madouer():
    def __init__(self, name):
        self.base = 'http://www.madouer.com'
        self.name = index[name]
        self.main_url = '%s%s' %(self.base, self.name)
    def CheckRemote(self):
        response = urllib.urlopen(self.main_url)
        html = response.read()
        soup = BeautifulSoup(html)
        NewList = soup.findAll('div', attrs={'class':'listbox'})
        if(NewList):
            down_month = []
            _new_baseurls = []
            lis = NewList[0].findAll('li')
            for li in lis:
                _l = li.findAll('a', attrs={'class':'pic'})
                new_baseurl =  self.base + str(_l[0]['href'])
                l = _l[0].find('img')
                _text = l['alt']
                text = _text.encode('utf-8').replace(' ', '')
                month = int(new_baseurl.split('/')[5] + new_baseurl.split('/')[6][:2])
                url_month = (new_baseurl, month, text)
                down_month.append(month)
                _new_baseurls.append(url_month)
            month = max(down_month)
            new_baseurls = []
            for i in _new_baseurls:
                if (i[0].split('/')[5] + i[0].split('/')[6][:2]) == str(month):
                    args = [self.name.split('/')[-2], i]
                    new_baseurls.append(args)
            return new_baseurls
        else:
            return None
    def getlist(self, LIST):
        a = self.CheckRemote()
        if a and len(a) > 0:
            LIST.append(a)


def vvshu_run(LIST):
    for h in LIST:
        for i in range(len(h)):
            _name =  h[i][0] + '_' + str(i+1)
            (url, month, text) = h[i][1]
            #print _name, url, month, text
            _begin_time = task_begin(_name)
            day = url.split('/')[-2]
            work_dir = CheckLocal(_name, day)
            if work_dir != None:
                htmfile = '%sview.htm' %work_dir
                cmd = 'rm -f %s' %htmfile
                os.system(cmd)
                add_head(htmfile)
                response = urllib.urlopen(url)
                html = response.read()
                out = html.split()
                out_len = len(out)
                p = re.compile(r'[0-9]{4}.*?\.jpg"$')
                for j in range(0,out_len):
                    if out[j] == 'page':
                        page = int(out[j+2][:-1])
                for k in out:
                    if p.match(k):
                        _tmp = k.split('=')[1].split('/')
                        _tmp_img_url = ''
                for l in range(len(_tmp)-1):
                    _tmp_img_url += _tmp[l] + '/'
                img_url = _tmp_img_url.replace('"','')
                msg = '[' + str(i+1) + '] Pages: ' + str(page) + ' [' + text + ']'
                print msg
                logger.info(msg)
                for m in range(1, page + 1):
                    _m = '%03d' %m
                    _img = _m + '.jpg'
                    img = img_url + _img
                    #weburl = url + '?' + _m
                    if os.path.exists('%s/%s' %(work_dir, _img)) == False:
                        cmd = 'wget -P %s %s' %(work_dir, img)
                        #os.system(cmd)
                        rc, out = commands.getstatusoutput(cmd)
                        #rc = 0
                        if rc != 0:
                            rc, out = commands.getstatusoutput(cmd)
                            if rc != 0:
                                rc, out = commands.getstatusoutput(cmd)
                    stdout_pre = sys.stdout
                    sys.stdout = Writer(htmfile)
                    print '<a href="%s" target=_blank><img border=0 src="%s"  onmousewheel="return zoompic(this);"></a><br><br>' %(_img, _img)
                    #print '<a target=_blank href="%s">%s</a>,978*1300<br>' %(_img, _img)
                    sys.stdout = stdout_pre
                cmd = 'ls %s | sed "s:^:%s/:"' %(work_dir[:-1], work_dir[:-1])
                rc, out = commands.getstatusoutput(cmd)
                if out != None:
                    file_count = int(len(out.split()))
                    file_list = out.split()
                cmd = 'du %s' %work_dir
                rc, out = commands.getstatusoutput(cmd)
                if out != None:
                    sum = int(out.split()[0])
                tar_count = (sum//(55*1024))+ 1
                fb = fenbao(file_count, tar_count)
                for n in range(0,len(fb)):
                    file_list_begin = fb[n][0]
                    file_list_end = fb[n][1]
                    files = file_list[file_list_begin-1:file_list_end]
                    fb_file_list = ''
                    for o in files:
                        fb_file_list += ' ' + o
                    _attr_path = '%s_%s.tar.gz' %(work_dir[:-1], str(n+1))
                    attr_path = ''.join(chr(ord(x)) for x in _attr_path)
                    if len(fb) == 1:
                        title = text + ' all'
                    else:
                        title = text + ' part ' + str(n+1) + ' of ' + str(len(fb))
                    if os.path.exists(attr_path)  == False:
                        cmd = 'cd %s && tar zcf %s %s' %(main_dir, attr_path, fb_file_list)
                        rc, out = commands.getstatusoutput(cmd)
                        if rc == 0:
                            Email(title, '', attr_path).run()
                            cmd = "echo /dev/null > %s" %attr_path
                            os.system(cmd)
                    #Email(title, '', attr_path).run() #test
            task_end(_name, _begin_time)


def madouer_run(LIST):
    base_img_url = 'http://img1.zazhimi.net/aazzmpic/'
    for h in LIST:
        for i in range(len(h)):
            _name =  h[i][0] + '_' + str(i+1)
            (url, month, text) = h[i][1]
            #print _name, url, month, text
            _begin_time = task_begin(_name)
            day = url.split('/')[5] + url.split('/')[6][:2]
            work_dir = CheckLocal(_name, day)
            if work_dir != None:
                htmfile = '%sview.htm' %work_dir
                cmd = 'rm -f %s' %htmfile
                os.system(cmd)
                add_head(htmfile)
                response = urllib.urlopen(url)
                html = response.read()
                out = html.split()
                out_len = len(out)
                for j in range(0,out_len):
                    if (out[j-1], out[j]) == ('var', 'page'):
                        page = int(out[j+2][:-1])
                    if (out[j-1], out[j]) == ('var', 'dir'):
                        dir = out[j+2][:-1].split("'")[1]
                msg = '[' + str(i+1) + '] Pages: ' + str(page) + ' [' + text + ']'
                img_url = base_img_url + dir
                print msg
                logger.info(msg)
                for m in range(1, page + 1):
                    _m = '%03d' %m
                    _img = _m + '.jpg'
                    img = img_url + _img
                    if os.path.exists('%s/%s' %(work_dir, _img)) == False:
                        cmd = 'wget -P %s %s' %(work_dir, img)
                        #os.system(cmd)
                        rc, out = commands.getstatusoutput(cmd)
                        #rc = 0
                        if rc != 0:
                            rc, out = commands.getstatusoutput(cmd)
                            if rc != 0:
                                rc, out = commands.getstatusoutput(cmd)
                    stdout_pre = sys.stdout
                    sys.stdout = Writer(htmfile)
                    print '<a href="%s" target=_blank><img border=0 src="%s"  onmousewheel="return zoompic(this);"></a><br><br>' %(_img, _img)
                    #print '<a target=_blank href="%s">%s</a>,978*1300<br>' %(_img, _img)
                    sys.stdout = stdout_pre
                cmd = 'ls %s | sed "s:^:%s/:"' %(work_dir[:-1], work_dir[:-1])
                rc, out = commands.getstatusoutput(cmd)
                if out != None:
                    file_count = int(len(out.split()))
                    file_list = out.split()
                cmd = 'du %s' %work_dir
                rc, out = commands.getstatusoutput(cmd)
                if out != None:
                    sum = int(out.split()[0])
                tar_count = (sum//(55*1024))+ 1
                fb = fenbao(file_count, tar_count)
                for n in range(0,len(fb)):
                    file_list_begin = fb[n][0]
                    file_list_end = fb[n][1]
                    files = file_list[file_list_begin-1:file_list_end]
                    fb_file_list = ''
                    for o in files:
                        fb_file_list += ' ' + o
                    _attr_path = '%s_%s.tar.gz' %(work_dir[:-1], str(n+1))
                    attr_path = ''.join(chr(ord(x)) for x in _attr_path)
                    if len(fb) == 1:
                        title = text + ' all'
                    else:
                        title = text + ' part ' + str(n+1) + ' of ' + str(len(fb))
                    if os.path.exists(attr_path)  == False:
                        cmd = 'cd %s && tar zcf %s %s' %(main_dir, attr_path, fb_file_list)
                        rc, out = commands.getstatusoutput(cmd)
                        if rc == 0:
                            Email(title, '', attr_path).run()
                            cmd = "echo /dev/null > %s" %attr_path
                            os.system(cmd)
                    #Email(title, '', attr_path).run() #test
            task_end(_name, _begin_time)
    


def fenbao(file_count, tar_count):
    last_1_begin = 1
    every_packge = (file_count/tar_count)
    last_1_end = (file_count/tar_count)
    li = []
    for i in range(0, tar_count):
        if i == tar_count - 1:
            arg = (((tar_count-1)*every_packge)+1, file_count)
            li.append(arg)
        else:
            arg = (last_1_begin, last_1_end)
            li.append(arg)
            last_1_begin += every_packge
            last_1_end += every_packge
    return li


def getcount(lis):
    a = {}
    for i in lis:
        a[i] = lis.count(i)
    return a


def rebuild():
    for i in _vvshu_list_2:
        for j in i:
            for k in _madouer_list_2:
                for l in k:
                    if (j[0] == l[0]):
                        if (j[1][1] >=l[1][1]):
                            _vvshus_1.append(j[0])
                        else:
                            _madouers_1.append(j[0])

							
class mylogger(object):
   def __init__(self,filename):
       self.filename = filename
   def initlog(self):
       logging.basicConfig(filename=self.filename,level = logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s')
       logger = logging.getLogger()
       return logger


if __name__ == '__main__':
    main_dir = '/tmp/magazine'
    log_dir = main_dir + '/logs'
    if os.path.exists(log_dir) == False:
        os.system("mkdir -p %s" %log_dir)
    today = str(date.today())
    logger = mylogger("%s/magazine-%s.log" %(log_dir, today)).initlog()
    logger.info("Start!!!")

    index = { 'spring':'/snjt/spring/',
              'jelly':'/tmxg/jelly/',
              'more':'/yyol/more/',
              'with':'/yyol/with/',
              'jj':'/yyol/jj/',
              'faxing':'/qtzz/faxing/',
              'biteki':'/qtzz/biteki/',
              'vivi':'/tmxg/vivi/',
              'cancam':'/yyol/cancam/',
              'mina':'/snjt/mina/',
              'nonno':'/snjt/nonno/'
    }

    _vvshus_1 = ['minacn', 'raycn', 'ray', '25ans', 'gisele', 'ginger', 'steady', 'sweet', 'meirenbaihua', 'vivicn']
    _madouers_1 = ['spring', 'jelly', 'with', 'jj', 'faxing', 'biteki']
    repeat = ['mina', 'nonno', 'vivi', 'cancam', 'more']

    [vvshu(t).getlist(_vvshu_list_2) for t in repeat] #create _vvshu_list_2
    [madouer(t).getlist(_madouer_list_2) for t in repeat] #create _madouer_list_2
    rebuild()

    [vvshu(t).getlist(_vvshu_list_1) for t in _vvshus_1] #create _vvshu_list_1
    [madouer(t).getlist(_madouer_list_1) for t in _madouers_1] #create _madouer_list_1

    print "#######################################################################"
    print _vvshus_1
    vvshu_run(LIST = _vvshu_list_1)
    
    print "#######################################################################"
    print _madouers_1
    madouer_run(LIST = _madouer_list_1)
