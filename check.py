#!/usr/bin/env python
import paramiko

codeCodes = {
    'black':     '0;30', 'bright gray':    '0;37',
    'blue':      '0;34', 'white':          '1;37',
    'green':     '0;32', 'bright blue':    '1;34',
    'cyan':      '0;36', 'bright green':   '1;32',
    'red':       '0;31', 'bright cyan':    '1;36',
    'purple':    '0;35', 'bright red':     '1;31',
    'yellow':    '0;33', 'bright purple':  '1;35',
    'dark gray': '1;30', 'bright yellow':  '1;33',
    'normal':    '0'
}

def stringc(text, color):
    """String in color."""
    return "\033["+codeCodes[color]+"m"+text+"\033[0m"

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


class check():
    def __init__(self, ips, devs, pa):
        self.ips = ips
        self.devs = devs
        self.pa = pa
    def run(self, cmds=None):
        for i in self.ips:
            cmd = 'hostname -f'
            r = para(i, self.pa).run(cmd)
            hostname = r.split()[0]
            print "%s %s" %(i, hostname)
            for j in self.devs:
                ip = 'Device Unknown'
                mac = 'Device Unknown'
                cmd = 'ifconfig %s' %j
                r = para(i, self.pa).run(cmd)
                if r == 1:
                    msg = 'Error: %s connect failed.' %i
                    print  stringc(msg, "green")
                    continue
                r_len = len(r.split())
                for k in range(0,r_len):
                    if r.split()[k] == 'inet':
                        ip = r.split()[k+1].replace('addr:','')
                    elif r.split()[k] == 'ether':
                        mac = r.split()[k+1]
                msg = "%s_ip: %s" %(j, ip)
                print  stringc(msg, "green")
                msg = "%s_mac: %s" %(j, mac)
                print  stringc(msg, "green")
            if cmds:
                for cmd in cmds:
                    msg = para(i, self.pa).run(cmd)
                    print  stringc(msg, "yellow")


if __name__ == '__main__':
    ips_1 = ["192.168.1.1", "192.168.1.2"]
    msg = "start to get info from ips_1..."
    print stringc(msg, "red")
    check(ips_1, ['em1', 'em2'], '123456').run()
    ips_2 = ["192.168.2.1", "192.168.2.2"]
    msg = "start to get info from ips_2, and run commands in ips_2..."
    print stringc(msg, "red")
    check(ips_2, ['br1'], '123456').run(['ipmitool chassis bootdev pxe', 'reboot'])
