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
        if add_devs is not None:
            if len(add_devs) > 0:
                for i,j in add_devs.items():
                    if len(j) == 4:
                        _add_gw = '--gateway %s' %j[3] if len(j[3])>0 else ''
                    elif len(j) == 3:
                        _add_gw = ''
                    cmd = 'cobbler system edit --name=%s --interface=%s --mac=%s --ip-address=%s --subnet=%s %s --static=1' %(hostname, i, j[0], j[1], j[2], _add_gw)
                    os.system(cmd)   #add dev
                    print 'Done => %s' %cmd
        kickstart=v.get('kickstart')
        if kickstart is not None:
            if len(kickstart) > 0:
                cmd = 'cobbler system edit --name=%s --kickstart=%s' %(hostname,kickstart)
                os.system(cmd)   #add kickstart
                print 'Done => %s' %cmd
        print '%s rebuild successfully.\n' %k
    print 'cobbler sync begin...'
    cmd = "cobbler sync"
    os.system(cmd)   #cobbler sync
    print 'cobbler sync successfully.'


##data
profile = "CentOS7.2-x86_64"
lis = {}
lis['B-control-1'] = {"hostname":"B-control-1",
    "ipmilan":("10.100.0.201", "root", "calvin"),
    "add_devs":{
    "em4":('f1:2a:72:da:88:d3', '10.100.0.101', '255.255.255.0'),
    },
    "kickstart":"/var/lib/cobbler/kickstarts/B.ks",
}
lis['B-cns-1'] = {"hostname":"B-cns-1",
    "ipmilan":("10.100.0.204", "root", "calvin"),
    "add_devs":{
    "em4":('f1:ba:db:31:7f:39', '10.100.0.104', '255.255.255.0'),
    },
    "kickstart":"/var/lib/cobbler/kickstarts/B.ks",
}
lis['B-nat-1'] = {"hostname":"B-nat-1",
    "ipmilan":("10.100.0.207", "root", "calvin"),
    "add_devs":{
    "em4":('f1:4d:a2:08:78:c3', '10.100.0.107', '255.255.255.0'),
    },
    "kickstart":"/var/lib/cobbler/kickstarts/B.ks",
}

##do
rebuild_system(profile, lis)
