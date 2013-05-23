#!/usr/bin/env python
import socket
import sys
import threading
import commands
import logging

SERVER = ''
RECVBUFLEN = 65535


class handler(threading.Thread):
    def __init__(self,socket,num):
        threading.Thread.__init__(self)
        self.socket = socket
        print 'thread started!'

    def run_command(self,cmd):
        rc, out = commands.getstatusoutput(cmd)
        if ( rc != 0 ):
            return False
        else:
            return True

    def run(self):
        while True:
            try:
                self.socket.listen(2)
            except socket.error, e:
               print 'Error listen socket: %s.' %e
               self.socket.close()
               return

            try:
                cs,address = self.socket.accept()
            except socket.error, e:
                print 'Error socket accept %s.' %e
                return

            recvstr = cs.recv(RECVBUFLEN)
            try:
                remote_ip = cs.getpeername()
            except:
                print 'connection is not established.'
                return
            if recvstr == '':
                cs.close()
                return

            try:
                arr =  recvstr.split()
            except:
                print 'msg can not be read.'
                cs.close()
                return

            if arr[0] not in ('nginx','mysql'):
                print 'permission denied, %s' %arr[0]
                cs.close()
                return
            cmd = '/etc/init.d/%s %s' %( arr[0], arr[1] )
            rc = self.run_command(cmd)
            if rc == True:
                print "Successful to run the command: %s, clinet is %s" % (cmd, remote_ip)
                logger.debug("Successful to run the command: %s, clinet is %s" % (cmd, remote_ip))
                cs.send("True")
            else:
                print "Failed to run the command: %s, clinet is %s" % (cmd, remote_ip)
                logger.debug("Failed to run the command: %s, clinet is %s" % (cmd, remote_ip))
                cs.send("Failed")
             
            cs.close()


class Server(object):
    def __init__(self,max_threads,server_port):
        self.socket = None
        self.max_threads = max_threads
        self.server_port = server_port
    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, e:
            print 'Error create socket: %s' %e
            logger.debug('Error create socket: %s' %e)
            sys.exit(1)

        try:
            self.socket.bind((SERVER,int(self.server_port)))
        except socket.error, e:
            print 'Error bind socket: %s' %e
            logger.debug('Error bind socket: %s' %e)
            self.socket.close()
            sys.exit(1)
        i = 0
        hdllist = []
        while i < int(self.max_threads):
            hdl = handler(self.socket,i)
            hdl.start()
            i = i + 1
            hdllist.append(hdl)
        for hdl in hdllist:
            hdl.join()


class mylogger(object):
   def __init__(self,filename):
       self.filename = filename
   def initlog(self):
       logging.basicConfig(filename=self.filename,level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
       logger = logging.getLogger()
       return logger


if __name__ == '__main__':
    max_threads = 3
    server_port = 3348
    logger=mylogger("/opt/app/server/log/server.log").initlog()
    startserver = Server(max_threads,server_port)
    startserver.run()
