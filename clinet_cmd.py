#!/usr/bin/env python
import getopt
import sys
import socket
import logging

RECVBUFLEN = 65535

def help():
    print 'Usage: python client_cmd.py -i $server_ip -s nginx|mysql -o start|stop|restart'
    sys.exit(1)

class mylogger(object):
   def __init__(self,filename):
       self.filename = filename
   def initlog(self):
       logging.basicConfig(filename=self.filename,level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
       logger = logging.getLogger()
       return logger


class client(object):
    def __init__(self):
        self.socket = None;

    def send(self,string):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except self.socket.error, e:
            print 'Create socket failure :%s' %e
            logger.debug('Create socket failure')
            sys.exit(1)

        try:
            self.socket.connect((SERVER,PORT))
        except:
            print 'Address error connecting to server %s' %SERVER
            logger.debug('Address error connection to server')
            sys.exit(1)

        try: 
            self.socket.send(string)
        except self.socket.error, e:
            print 'Error Sending the data: %s' %e
            logger.debug('Error Sending the data')
            sys.exit(1)

#        self.socket.settimeout(120)
        recvstr  = self.socket.recv(RECVBUFLEN)
        if recvstr == 'OK':
            print "Successful to run the command on Server."
            logger.debug("Successful to run the command on Server.")

        try:
            self.socket.close()
        except self.socket.error, e:
            print 'Error Closing the socket: %s' %e
            logger.debug('Error closing the socket')
            sys.exit(1)


if __name__ == '__main__':
    logger = mylogger("/opt/app/server/log/client.log").initlog()
    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:],"i:s:o:h",["ipaddr","script","option","help"])
        for param,value in opts:
            if param in ('-i','--ipaddr'):
                SERVER = value
            elif param in ('-s','--script'):
                script = value
            elif param in ('-o','--option'):
                option = value
            elif param in ('-h','--help'):
                help()
    else:
        help()
    PORT = 3348
    msg  = script + ' ' + option
    client().send(msg)
