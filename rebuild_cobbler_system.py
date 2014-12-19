#!/usr/bin/env python

import os

profile = "Centos7-cn0.ketong.com"

lis = {}
lis['cns-1'] = {"hostname":"cns-1.10.180.2.1.phy.cns.cn0.keytone",
                "ipmilan":("10.180.3.1", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:22:19:63:3d:b3', '10.180.2.1', '255.255.240.0'),
                    "em2":('f0:22:19:63:3d:b5', '10.180.17.1', '255.255.254.0'),
               }
}
lis['cns-2'] = {"hostname":"cns-2.10.180.2.2.phy.cns.cn0.keytone",
                "ipmilan":("10.180.3.2", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:ba:db:31:77:1e', '10.180.2.2', '255.255.240.0'),
                    "em2":('f0:ba:db:31:77:20', '10.180.17.2', '255.255.254.0'),
               }
}
lis['cns-3'] = {"hostname":"cns-3.10.180.2.3.phy.cns.cn0.keytone",
                "ipmilan":("10.180.3.3", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:ba:db:31:6f:5c', '10.180.2.3', '255.255.240.0'),
                    "em2":('f0:ba:db:31:6f:5e', '10.180.17.3', '255.255.254.0'),
               }
}
lis['nat-1'] = {"hostname":"nat-1.10.180.6.1.phy.nat.cn0.keytone",
                "ipmilan":("10.180.7.1", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:22:19:62:ed:70', '10.180.6.1', '255.255.240.0'),
                    "em2":('f0:22:19:62:ed:72', '10.180.16.1', '255.255.254.0'),
                    "em3":('f0:22:19:62:ed:74', '192.168.130.1', '255.255.255.0'),
               }
}
lis['nat-2'] = {"hostname":"nat-2.10.180.6.2.phy.nat.cn0.keytone",
                "ipmilan":("10.180.7.2", "root", "calvin"),
                "add_devs":{
                    "em1":('f0:2b:2b:05:4e:38', '10.180.6.2', '255.255.240.0'),
                    "em2":('f0:2b:2b:05:4e:3a', '10.180.16.2', '255.255.254.0'),
                    "em3":('f0:2b:2b:05:4e:3c', '192.168.130.2', '255.255.255.0'),
               }
}
lis['ceph-1'] = {"hostname":"ceph-1.10.180.4.1.phy.ceph.cn0.keytone",
                 "ipmilan":("10.180.5.1", "root", "calvin"),
                 "add_devs":{
                     "em1":('f0:ba:db:31:7f:33', '10.180.4.1', '255.255.240.0'),
                }
}
lis['ceph-2'] = {"hostname":"ceph-2.10.180.4.2.phy.ceph.cn0.keytone",
                 "ipmilan":("10.180.5.2", "root", "calvin"),
                 "add_devs":{
                     "em1":('f0:ba:db:38:b2:e8', '10.180.4.2', '255.255.240.0'),
                }
}
lis['ceph-3'] = {"hostname":"ceph-3.10.180.4.3.phy.ceph.cn0.keytone",
                 "ipmilan":("10.180.5.3", "root", "calvin"),
                 "add_devs":{
                     "em1":('f0:2b:cb:05:dc:07', '10.180.4.3', '255.255.240.0'),
                }
}
lis['ceph-4'] = {"hostname":"ceph-4.10.180.4.4.phy.ceph.cn0.keytone",
                 "ipmilan":("10.180.5.4", "root", "calvin"),
                 "add_devs":{
                     "em1":('f0:ba:db:31:86:ff', '10.180.4.4', '255.255.240.0'),
                }
}


def rebuild_system(pf, dic):
    for k,v in dic.items():
        print '%s begin rebuild...' %k
        hostname = v['hostname']
        cmd = 'cobbler system remove --name=%s' %hostname
        os.system(cmd)
        print 'Done => %s' %cmd
        ipmi_ip, ipmi_user, ipmi_password = v['ipmilan'][0:3]
        cmd = 'cobbler system  add --name=%s --hostname=%s --profile=%s --power-type=ipmilan --power-user=%s --power-pass=%s --power-address=%s'  %(hostname, hostname, pf, ipmi_user, ipmi_password, ipmi_ip)
        os.system(cmd)
        print 'Done => %s' %cmd
        add_devs = v.get('add_devs')
        if len(add_devs) > 0:
            for i,j in add_devs.items():
                cmd = 'cobbler system edit --name=%s --interface=%s --mac=%s --ip-address=%s --subnet=%s --static=1' %(hostname, i, j[0], j[1], j[2])
                os.system(cmd)
                print 'Done => %s' %cmd
        print '%s rebuild successfully.\n' %k
    print 'cobbler sync begin...'
    cmd = "cobbler sync"
    os.system(cmd)
    print 'cobbler sync successfully.'

rebuild_system(profile, lis)
