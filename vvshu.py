#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Thursday Sep 4 16:00 2014
@author: wangyucheng
'''

import sys, os
import commands
import re, time
import urllib
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


class Writer():
    def __init__(self, filename):
        self.filename = filename
    def write(self, msg):
        f = file(self.filename, 'a')
        f.write(msg)
        f.close()


class Email(object):
    def __init__(self, MAIL_SUBJECT, MAIL_MESSAGE, ATTACHMENT=None):
        self.MAIL_HOST = 'smtp.163.com'  #维护
        self.MAIL_USERNAME = '******@163.com'  #维护
        self.MAIL_PASSWORD = '******'  #维护
        self.MAIL_TO = '******@qq.com'  #维护
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
            print 'Send Email Successfully.'
        except Exception,e:
            print e


def  task_begin(name):
    _begin_time = datetime.now()
    begin_time = _begin_time.strftime("%Y-%m-%d %H:%M:%S")
    msg = "Downloading %s...BEGIN -- Current Time: %s" %(name, begin_time)
    print msg
    return _begin_time


def task_end(name, _begin_time):
    _end_time = datetime.now()
    end_time = _end_time.strftime("%Y-%m-%d %H:%M:%S")
    cost = (_end_time - _begin_time).seconds
    msg = "Downloading %s...END   -- Current Time: %s" %(name, end_time)
    print msg
    msg = "Downloading %s...Suc, Time Cost: %ss." %(name, cost)
    print msg


class Magazine():
    def __init__(self, name):
        self.name = name
        self.main_url = 'http://www.vvshu.com/view/%s/' %self.name
    def CheckLocal(self, day, d):
        work_dir = '%s/%s/%s_%s/' %(main_dir, day, self.name, d)
        if os.path.exists(work_dir) == False:
            os.system("mkdir -p %s" %work_dir)
        return work_dir
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
                new_baseurl = l[0]['href']
                month = int(new_baseurl.split('/')[5])
                url_month = (new_baseurl, month, li.text)
                down_month.append(month)
                _new_baseurls.append(url_month)
            month = max(down_month)
            new_baseurls = []
            for i in _new_baseurls:
                if i[0].split('/')[5] == str(month):
                    args = (i[0], i[2])
                    new_baseurls.append(args)
            return new_baseurls
        else:
            return None
    def add_head(self, filename):
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
    def run(self):
        baseurl = self.CheckRemote()
        if baseurl != None:
            if len(baseurl) != 0:
                _begin_time = task_begin(self.name)
                for k in range(len(baseurl)):
                    url, text = baseurl[k]
                    day = url.split('/')[-2]
                    work_dir = self.CheckLocal(day, k+1)
                    if work_dir != None:
                        htmfile = '%s/view.htm' %work_dir
                        cmd = 'rm -f %s' %htmfile
                        os.system(cmd)
                        self.add_head(htmfile)
                        response = urllib.urlopen(url)
                        html = response.read()
                        out = html.split()
                        out_len = len(out)
                        p = re.compile(r'[0-9]{4}.*?\.jpg"$')
                        for i in range(0,out_len):
                            if out[i] == 'page':
                                page = int(out[i+2][:-1])
                        for i in out:
                            if p.match(i):
                                _tmp = i.split('=')[1].split('/')
                                _tmp_img_url = ''
                        for j in range(len(_tmp)-1):
                            _tmp_img_url += _tmp[j] + '/'
                        img_url = _tmp_img_url.replace('"','')
                        print '[' + str(k+1) + '] Pages: ' + str(page) + ' [' + text + ']'
                        for i in range(1, page + 1):
                            _i = '%03d' %i
                            _img = _i + '.jpg'
                            img = img_url + _img
                            #weburl = url + '?' + _i
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
                        for i in range(0,len(fb)):
                            file_list_begin = fb[i][0]
                            file_list_end = fb[i][1]
                            files = file_list[file_list_begin-1:file_list_end]
                            fb_file_list = ''
                            for j in files:
                                fb_file_list += ' ' + j
                            _attr_path = '%s_%s.tar.gz' %(work_dir[:-1], str(i+1))
                            attr_path = ''.join(chr(ord(x)) for x in _attr_path)
                            if len(fb) == 1:
                                title = text + ' all'
                            else:
                                title = text + ' part ' + str(i+1) + ' of ' + str(len(fb))
                            if os.path.exists(attr_path)  == False:
                                cmd = 'cd %s && tar zcf %s %s' %(main_dir, attr_path, fb_file_list)
                                rc, out = commands.getstatusoutput(cmd)
                                if rc == 0:
                                    Email(title, '', attr_path).run()
                            #Email(title, '', attr_path).run() #test
                task_end(self.name, _begin_time)


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

	
if __name__ == '__main__':
    main_dir = '/tmp'
    [Magazine(t).run() for t in ['minacn', 'raycn', 'vivi', 'mina', 'nonno', 'ray', '25ans', 'cancam']]  #and so on...
