#!D:\Python27\python.exe
# -*- coding: utf-8 -*-

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

class Iqiyi:
    def __init__(self):
        pass
    def getItem(self, xxx):
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

def exchange(a):
    return a.decode('utf-8')

def getmovie(b, key):
    for m in b:
        if key == m['id']:
            name = m['name']
            turl = m['turl']
    return key,name,turl

if __name__ == "__main__":
    while 1:
        dramas = [{'id':1,'name':'来自星星的你','turl':'http://www.iqiyi.com/a_19rrgja8xd.html'},
                  {'id':2,'name':'识骨寻踪（第九季）','turl':'http://www.iqiyi.com/a_19rrifsvfq.html'}
        ]
        msg = "可以播放的剧集（Drama）: "
        print exchange(msg)
        for d in dramas:
            print str(d['id']) + ': ' + exchange(d['name'])
        userChoice = int(input('Choose a Drama: '))
        id,name,turl=getmovie(dramas,userChoice)
        reload(sys)
        sys.setdefaultencoding('gbk')
        dramaItems = Iqiyi().getItem(turl)
        for di in dramaItems:
            print di
        diLen = len(dramaItems)
        userChoice = int(input('Chose a number of the Drama: '))
        if userChoice >= 1 and userChoice <= diLen:
            dramaItems[userChoice-1].openDrama()
        time.sleep(1)
        os.system("cls")
