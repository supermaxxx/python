#!/usr/bin/env python

import os
import commands


##func
def rebuild_system(pf, dic):
    cmd = "cobbler system find"
    rc, out = commands.getstatusoutput(cmd)
    exists = out.split('\n') if len(out)>0 else None
    for k,v in dic.items():
        print '%s begin rebuild...' %k
        hostname = v['hostname']
        if exists != None:
            if v['hostname'] in exists:
                cmd = 'cobbler system remove --name=%s' %hostname
                os.system(cmd)   #remove a system
                print 'Done => %s' %cmd
        cmd = 'cobbler system  add --name=%s --hostname=%s --profile=%s' %(hostname, hostname, pf)
        os.system(cmd)   #create a system
        print 'Done => %s' %cmd
        if len(v['ipmilan']) > 0:
            ipmi_ip, ipmi_user, ipmi_password = v['ipmilan'][0:3]
            cmd = 'cobbler system edit --name=%s --power-type=ipmilan --power-user=%s --power-pass=%s --power-address=%s' %(hostname, ipmi_user, ipmi_password, ipmi_ip)
            os.system(cmd)   #add ipmilan
            print 'Done => %s' %cmd
        add_devs = v.get('add_devs')
        if len(add_devs) > 0:
            for i,j in add_devs.items():
                if len(j) == 4:
                    _add_gw = '--gateway %s' %j[3]
                elif len(j) == 3:
                    _add_gw = ''
                cmd = 'cobbler system edit --name=%s --interface=%s --mac=%s --ip-address=%s --subnet=%s %s --static=1' %(hostname, i, j[0], j[1], j[2], _add_gw)
                os.system(cmd)   #add dev
                print 'Done => %s' %cmd
        print '%s rebuild successfully.\n' %k
    print 'cobbler sync begin...'
    cmd = "cobbler sync"
    os.system(cmd)   #cobbler sync
    print 'cobbler sync successfully.'


##data
profile = "Centos7-cn0.ketong.com"
lis = {}
lis['cns-1'] = {"hostname":"cns-1.10.179.2.1.phy.cns.cntest.keytone",
                "ipmilan":("10.179.3.1", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:4d:a2:08:46:e1', '10.179.2.1', '255.255.0.0', '10.179.0.254'),
                }
}
lis['cns-2'] = {"hostname":"cns-2.10.179.2.2.phy.cns.cntest.keytone",
                "ipmilan":("10.179.3.2", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:22:19:61:e9:65', '10.179.2.2', '255.255.0.0', '10.179.0.254'),
                }
}
lis['nat-1'] = {"hostname":"nat-1.10.179.6.1.phy.nat.cntest.keytone",
                "ipmilan":("10.179.7.1", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:22:19:63:31:62', '10.179.6.1', '255.255.0.0'),
                }
}
lis['nat-2'] = {"hostname":"nat-2.10.179.6.2.phy.nat.cntest.keytone",
                "ipmilan":("10.179.7.2", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:22:19:62:34:15', '10.179.6.2', '255.255.0.0'),
                }
}

##do
rebuild_system(profile, lis)
