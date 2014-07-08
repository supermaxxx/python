#!/usr/bin/python

import telnetlib

Host = '173.20.11.254'
password = 'huawei'
finish = '<ZWWW-S7706-1>'
comfirm = 'continue?[Y/N]:'

cmd = 'reset arp all'
yes = 'Y'

tn = telnetlib.Telnet(Host)      
    
print 'Start to login with Password'

tn.read_until('Password:')  
tn.write(password + '\n')  

print 'Logined!'
   
tn.read_until(finish)
tn.write(cmd + '\n')

print 'Comfirm arp all reset!'
tn.read_until(comfirm)
tn.write(yes + '\n')

print 'Complete to arp reset!'
tn.read_until(finish)
tn.close()
