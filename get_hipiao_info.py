#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Fri Feb 14 17:30 2014
@author: wangyucheng
'''

import urllib
from bs4 import BeautifulSoup
from datetime import date, timedelta

def cs(a):
    return a.decode('utf-8')

today = date.today()
tomorrow = today + timedelta(1)
days = [str(today),str(tomorrow)]
url = 'http://cinema.hipiao.com/dadi_jiading'
response = urllib.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
for day in days:
    msg = cs("<大地数字影院--上海嘉定罗宾森广场--电影排片表--%s>\n\n" %(day.replace('-','/')))
    movieList = soup.findAll('div', attrs={'id':'planDataList'})
    if(movieList):
        lis = movieList[0].findAll('li', attrs={'day':day})
        for li in lis:
            #pm = li.find('div').text    #片名(地区)
            pm = li['film']    #片名
            ps = li.findAll('p')
            pcs = ps[3].text.split()
            pc = pcs[2] if len(pcs)==3 else 'Unknown'    #片长
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
                msg += cs('放映时间 语种/制式 会员价/原价: \n') 
                for tds in tr:
                    td = tds.findAll('td')
                    if len(td) > 0:
                        sijian = td[0].text    #放映时间
                        yuyan = td[1].text    #语种/制式
                        jiage =  td[4].text[1:] + cs('元/') + td[3].text[1:-3] + cs('元')    #会员价/原价
                        msg += sijian + '    ' + yuyan + ' ' + jiage + '\n'
            msg += '\n'
    m = msg.encode('utf-8')
    print m



'''
result:
[root@localhost test]# date
Sun Feb 16 20:07:03 CST 2014
[root@localhost test]# python get_hipiao_info.py 
<大地数字影院--上海嘉定罗宾森广场--电影排片表--2014/02/16>

片名: 澳门风云
片长: 95分钟
导演: 王晶
演员: 周润发,谢霆锋
地区: 中国,中国香港
放映时间 语种/制式 会员价/原价: 
20:40    国语/数字 35元/45元
21:30    国语/数字 35元/45元

片名: 北京爱情故事
片长: Unknown
导演: 陈思诚
演员: 梁家辉,刘嘉玲
地区: 中国
放映时间 语种/制式 会员价/原价: 
22:20    国语/数字 35元/45元

片名: 林中小屋
片长: 95分钟
导演: 邓特希
演员: 王宗尧,李昕岳
地区: 中国,中国香港
放映时间 语种/制式 会员价/原价: 
22:30    国语/数字 35元/45元

片名: 西游记之大闹天宫
片长: 120分钟
导演: 郑保瑞
演员: 甄子丹,周润发
地区: 中国,中国香港,美国
放映时间 语种/制式 会员价/原价: 
21:40    国语/3D立体 35元/45元


<大地数字影院--上海嘉定罗宾森广场--电影排片表--2014/02/17>

片名: 澳门风云
片长: 95分钟
导演: 王晶
演员: 周润发,谢霆锋
地区: 中国,中国香港
放映时间 语种/制式 会员价/原价: 
12:10    国语/数字 30元/40元
14:00    国语/数字 30元/40元
15:45    国语/数字 30元/40元
17:40    国语/数字 30元/40元
19:30    国语/数字 35元/45元
21:20    国语/数字 35元/45元

片名: 爸爸去哪儿
片长: 95分钟
导演: 谢涤葵,林妍
演员: 林志颖,小小志
地区: 中国
放映时间 语种/制式 会员价/原价: 
11:30    国语/数字 35元/45元
13:20    国语/数字 35元/45元
17:10    国语/数字 35元/45元
19:00    国语/数字 40元/50元

片名: 北京爱情故事
片长: Unknown
导演: 陈思诚
演员: 梁家辉,刘嘉玲
地区: 中国
放映时间 语种/制式 会员价/原价: 
11:40    国语/数字 30元/40元
13:50    国语/数字 30元/40元
16:00    国语/数字 30元/40元
18:10    国语/数字 35元/45元
20:20    国语/数字 35元/45元

片名: 冰雪奇缘
片长: 108分钟
导演: 克里斯·巴克,珍妮弗·李
演员: 克里斯汀·贝尔,伊迪娜·门泽尔
地区: 美国
放映时间 语种/制式 会员价/原价: 
11:20    英语/数字 25元/35元
15:10    英语/数字 25元/35元

片名: 林中小屋
片长: 95分钟
导演: 邓特希
演员: 王宗尧,李昕岳
地区: 中国,中国香港
放映时间 语种/制式 会员价/原价: 
22:30    国语/数字 35元/45元

片名: 西游记之大闹天宫
片长: 120分钟
导演: 郑保瑞
演员: 甄子丹,周润发
地区: 中国,中国香港,美国
放映时间 语种/制式 会员价/原价: 
13:10    国语/3D立体 30元/40元
15:20    国语/3D立体 30元/40元
17:30    国语/3D立体 30元/40元
19:40    国语/3D立体 35元/45元
20:40    国语/3D立体 35元/45元
21:50    国语/3D立体 35元/45元


'''
