#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup

#def a(b):
#    return b.encode('utf-8').replace('<p align="center">','')[:-4]

url = 'http://bbs.anzhi.com/thread-8278415-1-1.html'
response = urllib.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
diziList = soup.findAll('table', attrs={'class':'t_table'})
if(diziList):
    lis = diziList[0].findAll('p')
    num = len(lis) - 1
    i = 0
    for li in lis:
        i += 1
        if i%2 == 0:
            print li.text
        else:
            print li.text + " ==",
