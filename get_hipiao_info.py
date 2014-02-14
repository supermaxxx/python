#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 17:30 2014
@author: wangyucheng
"""

import urllib
from bs4 import BeautifulSoup
from datetime import date, timedelta

def cs(a):
    return a.decode('utf-8')

now = date.today()
tomorrow = now + timedelta(1)
days = [str(now),str(tomorrow)]
url = 'http://cinema.hipiao.com/dadi_jiading'
response = urllib.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
for w in days:
    msg = cs("大地数字影院--上海嘉定罗宾森广场--电影排片表--%s\n\n" %(w.replace('-','/')))
    movieList = soup.findAll('div', attrs={'id':'planDataList'})
    if(movieList):
        lis = movieList[0].findAll('li', attrs={'day':w})
        for li in lis:
            pm = li.find('div').text    #片名
            ps = li.findAll('p')
            pcs = ps[3].text.split()
            pc = pcs[2] if len(pcs)==3 else 'Unknown'    #片长
            dy = ps[0].text.replace(' / ',',').split()[2]    #导演
            yys = ps[1].text.replace(' / ',',').split()[1].split(',')    #演员
            yy = yys[0] + ',' + yys[1] if len(yys) > 1 else yys[0]    #演员（取最多前2个）
            dq = ps[2].text.replace(' ',',').split()[2].replace(',','')    #地区
            msg += cs('片名:') + pm + '\n'
            msg += cs('片长:') + pc + '\n'
            msg += cs('导演:') + dy + '\n'
            msg += cs('演员:') + yy + '\n'
            msg += cs('地区:') + dq + '\n'
            cts = li.findAll('div', attrs={'class':'ciname_table'})
            for ct in cts:
                tr = ct.findAll('tr')
                msg += cs('放映时间 语种/制式 会员价/原价')  + '\n'
                for tds in tr:
                    td = tds.findAll('td')
                    if len(td) > 0:
                        sijian = td[0].text    #放映时间
                        yuyan = td[1].text    #语种/制式
                        jg = td[4].text[1:] + cs('元/') + td[3].text[1:-3] + cs('元')    #会员价/原价
                        msg += sijian + ' ' + yuyan + ' ' + jg + '\n'
            msg += '\n'
    m = msg.encode('utf-8')
    print m
