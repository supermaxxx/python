#!/usr/bin/env python

import os
from lib.common_lib import mylogger

def check_proc():
    for proc_name in proc_names:
        ps_str = 'ps aux |grep %s | grep -v grep' %proc_name
        x= os.popen(ps_str).read()
        if x :
            pass
        else: 
            if (proc_name == proc_names[0]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/etc/init.d/mysql start')
            if (proc_name == proc_names[1]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/etc/init.d/nginx start')
            if (proc_name == proc_names[2]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/etc/init.d/dhcpd start')
            if (proc_name == proc_names[3]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/etc/init.d/xinetd start')
            if (proc_name == proc_names[4]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/etc/init.d/php-fpm start')
            if (proc_name == proc_names[5]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/usr/bin/python /opt/app/server/server.py &')
            if (proc_name == proc_names[6]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/usr/bin/python /opt/app/server/bmc_check.py &')
            if (proc_name == proc_names[7]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/etc/init.d/shellinabox start')
            if (proc_name == proc_names[8]):
                logger.debug('Can not find proc: %s, start it!' %proc_name)
                os.system('/etc/init.d/vncserver start')

if __name__=='__main__':
    proc_names = 'mysql','nginx','dhcp','xinetd','php','server.py','bmc_check.py','shellinaboxd','vnc'
    logger = mylogger("/opt/log/process.log").initlog()
    check_proc()
