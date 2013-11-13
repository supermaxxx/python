#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Created on Thur Nov 7 14:00 2013
@author: wangyucheng
@Useage: python random_ip_mac.py 6000
"""

import random
import sys
from mylib.common_lib import mysql
from mylib.common_lib import writelogfile

def randomMAC():
    mac = [ 0x52, 0x54, 0x00,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac)).upper()

def randomIP():
    ip  = [ 10, 100,
            random.randint(0, 200),
            random.randint(2, 200) ]
    return '.'.join(map(lambda x: str(x), ip))

_listIP = _listMAC = _xlist = _ylist = []

n = int(sys.argv[1])
n_try = int(n * 1.5)

if n_try > 39600:
    print "too many"
    sys.exit(0)

for i in range(1,n_try+1):
    _listIP.append(randomIP())
    _listMAC.append(randomMAC())

listIP = listMAC = []
[listIP.append(i) for i in _listIP if not i in listIP]
[listMAC.append(i) for i in _listMAC if not i in listMAC]
len_listIP = len(listIP)
len_listMAC = len(listMAC)

if len_listIP < len_listMAC:
    len_test = len_listIP
    cha = len_listIP - len_listMAC
    del listMAC[cha:]
elif len_listIP > len_listMAC:
    len_test = len_listMAC
    cha = len_listMAC - len_listIP
    del listIP[cha:]
elif len_listIP == len_listMAC:
    len_test = len_listIP

if len_test > n:
    cha = n - len_test
    del listIP[cha:]
    del listMAC[cha:]
elif len_test < n:
    print "please try again."
    sys.exit(0)

msg = ''
for i in range(n):
    line = 'insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values (' + "'" + listIP[i] + "','" + listMAC[i] + "',"+ '1, 0, 0);\n'
    msg+=line
writelogfile('10.100_ip.sql').log(msg)
