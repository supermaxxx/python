#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Created on Thur Nov 7 14:00 2013
@author: wangyucheng
@Useage: python random_ip_mac.py 6000    #1-26400
"""

import random
import os
import sys
from mylib.common_lib import mysql
from mylib.common_lib import writelogfile

file = '10.100_ip.sql'
if os.path.exists(file):
    os.system("rm -f %s" %file)

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

_listIP = []
_listMAC = []
_xlist = []
_ylist = []

n = int(sys.argv[1])
n_try = int(n * 1.5)

if n_try > 39600:
    print "too many, please use 1-26400"
    sys.exit(0)

for i in range(1,n_try+1):
    _listIP.append(randomIP())
    _listMAC.append(randomMAC())

listIP = []
listMAC = []
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
    print "Target is %s, get %s. Successfully!\nresult is in the file %s(%s lines)." %(n,n,file,n)
elif len_test < n:
    cha = len_test -n
    n_old = n
    n = len_test
    print "Target is %s, but get %s. If you want target, please have another try as: ./radom_ip_mac.py %s\nresult is in the file %s(%s lines)." %(n_old,n,n_old,file,n)

msg = ''
for i in range(n):
    line = 'insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values (' + "'" + listIP[i] + "','" + listMAC[i] + "',"+ '1, 0, 0);\n'
    msg+=line
writelogfile(file).log(msg)

'''
[root@10-9-12-126 wang]# python r.py 100         
Target is 100, get 100. Successfully!
result is in the file 10.100_ip.sql(100 lines).
[root@10-9-12-126 wang]# cat 10.100_ip.sql |wc -l
100

[root@10-9-12-126 wang]# python r.py 1000
Target is 1000, get 1000. Successfully!
result is in the file 10.100_ip.sql(1000 lines).
[root@10-9-12-126 wang]# cat 10.100_ip.sql |wc -l
1000

[root@10-9-12-126 wang]# python r.py 25000       
Target is 25000, but get 24306. If you want target, please have another try as: ./radom_ip_mac.py 25000
result is in the file 10.100_ip.sql(24306 lines).
[root@10-9-12-126 wang]# cat 10.100_ip.sql |wc -l
24306

[root@10-9-12-126 wang]# python r.py 26401
too many, please use 1-26400

[root@10-9-12-126 wang]# cat 10.100_ip.sql 
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.45.37','52:54:00:55:B8:CE',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.1.4','52:54:00:76:18:3A',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.58.107','52:54:00:1B:0F:EA',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.150.183','52:54:00:5B:31:6B',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.165.115','52:54:00:61:C0:88',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.81.123','52:54:00:09:0A:32',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.46.195','52:54:00:50:59:3C',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.55.53','52:54:00:28:05:AF',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.14.140','52:54:00:75:23:AD',1, 0, 0);
insert into wang_ip_resource (ip, mac, zone_id, operator_id, state) values ('10.100.121.198','52:54:00:2F:78:A4',1, 0, 0);
...
'''
