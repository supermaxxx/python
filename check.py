#!/usr/bin/env python
import paramiko

class para(object):
    def __init__(self, ip, pa):
        self.hostname = ip
        self.username = 'root'
        self.password = pa
    def getconn_ssh(self):
        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conn.connect(hostname = self.hostname, username = self.username, password = self.password)
        return self.conn
    def get_response(self, cmd):
        try:
            self.getconn_ssh()
        except:
            print "Conn error."
        stdin,stdout,stderr = self.conn.exec_command(cmd)
        result =  stdout.read()
        self.conn.close()
        return result
    def run(self, cmd):
        try:
            self.getconn_ssh()
        except Exception:
            return 1
        else:
            stdin,stdout,stderr = self.conn.exec_command(cmd)
            result=stdout.read()
            self.conn.close()
            return result


class run():
    def __init__(self, ips, dev, pa):
        self.ips = ips
        self.dev = dev
        self.pa = pa
    def run(self, cmds=None):
        for i in self.ips:
            cmd = 'ifconfig %s' %self.dev
            if r == 1:
                print 'Error: %s connect failed.' %i
                continue
            r = para(i, self.pa).run(cmd)
            r_len = len(r.split())
            for j in range(0,r_len):
                if r.split()[j] == 'inet':
                    ip=r.split()[j+1].replace('addr:','')
            cmd = 'hostname -f'
            r = para(i, self.pa).run(cmd)
            hostname = r.split()[0]
            print "%s %s" %(ip, hostname)
            if cmds:
                for cmd in cmds:
                    print para(i, self.pa).run(cmd)


if __name__ == '__main__':
    ips_1 = ["192.168.1.1", "192.168.1.2"]
    run(ips_1, 'em1', '123456').run()
    ips_2 = ["192.168.2.1", "192.168.2.2"]
    run(ips_2, 'br1', '123456').run(['ipmitool chassis bootdev pxe', 'reboot'])
