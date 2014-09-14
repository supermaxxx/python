#!/usr/bin/env python
import json
import urllib2

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
        self.api_data['params']= params
        return self._request()


if __name__ == "__main__":
    api_info = {
            'url': 'http://192.168.200.25/zabbix/api_jsonrpc.php',
            'user':'admin',
            'password':'zabbix'
    }

    zapi = ZabbixApi(api_info)

    #usergroup admin info
    tmp = zapi.run("usergroup.getobjects", {"output":"extend", "name":"zabbix administrators"})
    user_groupid_of_admin = tmp['result'][0]['usrgrpid'] if len(tmp['result'])>0 else None  #require to create admin user

    #create an admin user "wangyucheng" if not exist  [require: usergroup_id]
    new_user = {"name":"wangyucheng",
                "alias":"wangyucheng",
                "passwd":"wangyucheng",
                "usrgrps":{"usrgrpid":user_groupid_of_admin},
                "user_medias":[{"mediatypeid":1,
                                "sendto":"wangyucheng@keytonecloud.com",
                                "active":0,
                                "severity": 63,
                                "period": "1-7,00:00-24:00"
                }]
    }
    tmp = zapi.run("user.get", {"output":"extend"})
    all_users = tmp['result'] if len(tmp['result'])>0 else None
    u = 0
    for user in all_users:
        if user['alias'] == new_user['name']:
            u += 1
    if u == 0:
        zapi.run("user.create", new_user)
        print "create user %s successfully." %new_user['name']

    #create a hostgroup "test1" if not exist
    new_hostgroup_name = "test1"
    tmp = zapi.run("hostgroup.exists", {"name":new_hostgroup_name})
    if tmp['result'] == False:
        zapi.run("hostgroup.create", {"name":new_hostgroup_name})
        print "create hostgroup %s successfully." %new_hostgroup_name
    tmp = zapi.run("hostgroup.getobjects", {"name":new_hostgroup_name})
    new_hostgroup_id = tmp['result'][0]['groupid'] if len(tmp['result'])>0 else None  #require to create host/template

    #create a template "Template RAID for group test1"  [require: hostgroup_id]
    new_template_name = "Template RAID for hostgroup test1"
    tmp = zapi.run("template.exists", {"name":new_template_name})
    if tmp['result'] == False:
        zapi.run("template.create", {"host":new_template_name, "groups":{"groupid":new_hostgroup_id}})
        print "create template %s successfully." %new_template_name
    tmp = zapi.run("template.getobjects", {"host":new_template_name})
    new_template_id = tmp['result'][0]['templateid'] if len(tmp['result'])>0 else None  #require to create host/item

    #create any hosts and items  [require:hostgroup_id, template_id]
    new_hosts = {"test2":"192.168.110.2","test8":"192.168.110.8"}
    for (k, v) in new_hosts.items():
        #create a host
        tmp = zapi.run("host.exists", {"host":k})
        if tmp['result'] == False:
            zapi.run("host.create", {"host":k, 
                                     "interfaces":[{"type":1,"main":1,"useip":1,"ip":v,"dns": "","port": "10050"}],
                                     "groups":[{"groupid":new_hostgroup_id}],
                                     "templates":[{"templateid":new_template_id}]
                     }                 
            )
            print "create host successfully. (hostname:%s, ip:%s)" %(k,v)
        tmp = zapi.run("host.getobjects", {"host":k})
        new_host_id = tmp['result'][0]['hostid'] if len(tmp['result'])>0 else None
        tmp = zapi.run("hostinterface.get", {"output":"extend", "hostids":new_host_id})
        new_interface_id = tmp['result'][0]['interfaceid'] if len(tmp['result'])>0 else None
        #create 3 items
        new_item = {
            "interfaceid":new_interface_id,
            "hostid":new_template_id,
            "type":0,
            "value_type":3,
            "data_type":0,
            "delay":60
        }
        new_item['name'] = "Raid.info"
        new_item['key_'] = "Raid.info"
        tmp = zapi.run("item.exists", {"hostid":new_item['hostid'], "key_":new_item['key_']})
        if tmp['result'] == False:
            zapi.run("item.create", new_item)
            print "create key:%s of template:%s successfully." %(new_item['key_'], new_template_name)
        new_item['name'] = "Raid.disk.error"
        new_item['key_'] = "Raid.disk.error"
        tmp = zapi.run("item.exists", {"hostid":new_item['hostid'], "key_":new_item['key_']})
        if tmp['result'] == False:
            zapi.run("item.create", new_item)
            print "create key:%s of template:%s successfully." %(new_item['key_'], new_template_name)
        new_item['name'] = "Raid.Error_Count"
        new_item['key_'] = "Raid.Error_Count"
        tmp = zapi.run("item.exists", {"hostid":new_item['hostid'], "key_":new_item['key_']})
        if tmp['result'] == False:
            zapi.run("item.create", new_item)
            print "create key:%s of template:%s successfully." %(new_item['key_'], new_template_name)
