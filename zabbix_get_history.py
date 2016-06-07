#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
import os,sys
import time,datetime
import re
import logging

class ZabbixApi:
    def __init__(self,api_info):
        self.api_info = api_info
        self.header = {"Content-Type": "application/json"}
        self.api_data = {
                'jsonrpc':'2.0',
                'method':'',
                'params':'',
                'id':0
                }
        self._set_auth_session()
    def _set_auth_session(self):
        self.api_data['method'] = 'user.login'
        self.api_data['params']= {
                          'user':self.api_info['user'],
                          'password':self.api_info['password']
                        }
        response = self._request()
        self.api_data['auth'] = response['result']
        self.api_data['id'] = 1
    def _request(self):
        post_data = json.dumps(self.api_data)
        req = urllib2.Request(self.api_info['url'],post_data)
        for k,v in self.header.items():
            req.add_header(k,v)
        try:
            result = urllib2.urlopen(req)
        except urllib2.URLError as e:
            print e.code
        else:
            response = json.loads(result.read())
            result.close()
            return response
    def run(self,method,params):
        self.api_data['method'] = method
        self.api_data['params'] = params
        return self._request()


class writelogfile(object):
    def __init__(self,logname):
        self.logfilename = logname
    def log(self,logmsg):
        fd = open(self.logfilename, 'a')
        _logmsg = "%s\n" %(logmsg)
        fd.write(_logmsg)
        fd.close()


if __name__ == "__main__":
    api_info = {
            'url': 'http://192.168.1.200/zabbix/api_jsonrpc.php',
            'user':'admin',
            'password':'xxxxxx'
    }
    zapi=ZabbixApi(api_info)
    args=[
        ##add {host:[([key1,key2...],history_object_type1),([key5,key6...],history_object_type2),...]},
        ##history_object_type: 0-float; 1-string; 2-log; 3-integer; 4-text. 
        {"cns-1":[(["system.cpu.load[percpu,avg1]","system.cpu.load[percpu,avg5]"],0),
                  (["vm.memory.size[available]"],3),
                 ]},
        {"cns-2":[(["system.cpu.load[percpu,avg1]","system.cpu.load[percpu,avg5]"],0),
                  (["vm.memory.size[available]"],3),
                 ]},
        {"cns-3":[(["system.cpu.load[percpu,avg1]","system.cpu.load[percpu,avg5]"],0),
                  (["vm.memory.size[available]"],3),
                 ]},
    ]
    try:
        _clock_begin,_clock_end=str(sys.argv[1]),str(sys.argv[2])
    except:
        print 'Usage: python %s "2016-05-01 00:00:00" "2016-05-31 23:59:59"'  %(sys.argv[0])
        sys.exit(1)
    clock_begin=time.mktime(time.strptime(_clock_begin,"%Y-%m-%d %H:%M:%S"))
    clock_end=time.mktime(time.strptime(_clock_end,"%Y-%m-%d %H:%M:%S"))
    logfile="/tmp/data_%s_to_%s.csv" %(_clock_begin.replace(" ","-"),_clock_end.replace(" ","-"))
    if os.path.exists(logfile):
        os.remove(logfile)
    data=[]
    msg='"HOST","KEY","VAULE","CLOCK"'
    writelogfile(logfile).log(msg)
    for arg in args:
        for host,keys in arg.items():
            tmp=zapi.run("host.get",{"output":["hostid"],"filter":{"host":host}})
            if tmp["result"]==[]:
                continue
            host_id=tmp["result"][0]["hostid"]
            for _key in keys:
                dic={}
                key=_key[0]
                history_object_type=int(_key[1])
                itemids=[]
                for k in key:
                    tmp=zapi.run("item.get",{"output":"itemids","hostids":host_id,"search":{"key_":k}})
                    if tmp["result"]==[]:
                        continue
                    item_id=tmp["result"][0]["itemid"]
                    dic[item_id]=k
                    itemids.append(item_id)
                print "\n\033[0;32m%s\033[0m"  %("Host:"+str(host)+" Key:"+str(key)+" Itemid:"+str(itemids))
                tmp=zapi.run("history.get",{"history":history_object_type,"itemids":itemids,"output":"extend",
                             "time_from":clock_begin,"time_till":clock_end})
                _data=tmp["result"]
                print host+": "+str(key)+" "+str(len(_data))+" rows"
                for i in _data:
                    d={}
                    value=i["value"]
                    _clock=i["clock"]
                    clock=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(_clock)))
                    k=dic[i["itemid"]]
                    d["key"]=k
                    d["host"]=host
                    d["value"]=value
                    d["clock"]=clock
                    data.append(d)
                    msg='"%s","%s","%s","%s"' %(host,k,value,clock)
                    writelogfile(logfile).log(msg)
    print "%s is the output data file." %logfile
    #print len(data)  #it is the data u want.
