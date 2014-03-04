#!D:\Python27\python.exe
# -*- coding: utf-8 -*-
#目前支持iqiyi和pps,其中一些js生成的domain信息无法抓取

import time
import sys
import urllib
import os
from bs4 import BeautifulSoup

class DramaItem:
    def __init__(self, num, title, url):
        self.num = num
        self.title = title
        self.url = url
    def __str__(self):
        return self.num + '    ' + self.title
    def openDrama(self):
        os.startfile(self.url)

class Drama(object):
    def __init__(self,dramas):
        self.dramas = dramas
    def getItem_iqiyi(self, xxx):
        reload(sys)
        sys.setdefaultencoding('gbk')
        response = urllib.urlopen(xxx)
        html = response.read()
        soup = BeautifulSoup(html)
        dramaList = soup.findAll('div', attrs={'class':'list_block1 align_c'})
        dramaItems = []
        if(dramaList):
            lis = dramaList[0].findAll('li')
            for li in lis:
                ps = li.findAll('p')
                description = ps[1].text if len(ps)>1 else ''
                num = ps[0].find('a').text
                url = ps[0].find('a')['href']
                di = DramaItem(num, description, url)
                dramaItems.append(di)
        return dramaItems
    def getItem_pps(self, xxx):
        response = urllib.urlopen(xxx)
        html = response.read()
        soup = BeautifulSoup(html)
        dramaList = soup.findAll('ul', attrs={'class':'p-list128-80 p-list2'})
        dramaItems = []
        if(dramaList):
            lis = dramaList[0].findAll('div', attrs={'class':'t'})
            for li in lis:
                ps = li.find('a')
                num = ps.text.split()[1].encode('utf-8')
                description = ''
                url = ps['href'][:-11]
                di = DramaItem(num, description, url)
                dramaItems.append(di)
        return dramaItems
    def run(self):
        while 1:
            msg = "可以播放的剧集（Drama）: "
            print exchange(msg)
            for d in self.dramas:
                print str(d['id']) + ': ' + exchange(d['name'])
	        msg = "Choose a Drama: "
            userChoice = inputMsg(msg)
            dLen = len(self.dramas)
            if userChoice >= 1 and userChoice <= dLen:
                id,region,name,turl = getdrama(self.dramas, userChoice)
            else:
                print 'Input Error.'
                continue
            if region == 'iqiyi':
                dramaItems = self.getItem_iqiyi(turl)
            elif region == 'pps':
                dramaItems = self.getItem_pps(turl)
            for dd in dramaItems:
                print dd
            diLen = len(dramaItems)
            msg = "Chose a number of the Drama: "
            userChoice = inputMsg(msg)
            if userChoice >= 1 and userChoice <= diLen:
                dramaItems[userChoice-1].openDrama()
                time.sleep(1)
            else:
                print 'Input Error.'
                continue
            os.system("cls")

def inputMsg(msg):
    _userChoice = raw_input(msg)
    if (type(_userChoice)==type('')):
        if(_userChoice == 'q' or _userChoice == 'quit'):
            print 'quit...'
            sys.exit(0)
    try:
        userChoice = int(_userChoice)
    except Exception:
        sys.exit(1)
    return userChoice

def exchange(a):
    return a.decode('utf-8')

def getdrama(b, key):
    for m in b:
        if key == m['id']:
            region = m['region']
            name = m['name']
            turl = m['turl']
    return key,region,name,turl


if __name__ == "__main__":
    dramas = [{'id':1,'region':'iqiyi','name':'来自星星的你','turl':'http://www.iqiyi.com/a_19rrgja8xd.html'},
              {'id':2,'region':'iqiyi','name':'识骨寻踪（第九季）','turl':'http://www.iqiyi.com/a_19rrifsvfq.html'},
              {'id':3,'region':'pps','name':'诈欺猎人','turl':'http://v.pps.tv/splay_137983.html'},
    ]
    Drama(dramas).run()
