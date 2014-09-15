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
            'url': 'http://1.1.1.1/zabbix/api_jsonrpc.php',
            'user':'admin',
            'password':'admin'
    }

    zapi = ZabbixApi(api_info)

    #usergroup admin info
    tmp = zapi.run("usergroup.getobjects", {"output":"extend", "name":"zabbix administrators"})
    user_groupid_of_admin = tmp['result'][0]['usrgrpid'] if len(tmp['result'])>0 else None  #require to create admin user

    #create a admin user "wangyucheng" if not exist  [require: usergroup_id]
    new_user = {"name":"wangyucheng",
                "alias":"wangyucheng",
                "passwd":"wangyucheng",
                "usrgrps":{"usrgrpid":user_groupid_of_admin},
                "user_medias":[{"mediatypeid":1,
                                "sendto":"wangyucheng@demo.com",
                                "active":0,
                                "severity": 63,
                                "period": "1-7,00:00-24:00"
                }]
    }
    tmp = zapi.run("user.get", {"output":"extend"})
    all_users = tmp['result'] if len(tmp['result'])>0 else None
    u = 0
    for user in all_users:
        if user['name'] == new_user['name']:
            u += 1
    if u == 0:
        zapi.run("user.create", new_user)
        print "create user '%s' successfully." %new_user['name']
    tmp = zapi.run("user.get", {"output":"extend"})
    all_users = tmp['result'] if len(tmp['result'])>0 else None
    for user in all_users:
        if user['name'] == new_user['name']:
            new_user_id = user['userid']

    #create a hostgroup "Physical Machine" if not exist
    new_hostgroup_name = "Physical Machine"
    tmp = zapi.run("hostgroup.exists", {"name":new_hostgroup_name})
    if tmp['result'] == False:
        zapi.run("hostgroup.create", {"name":new_hostgroup_name})
        print "create hostgroup '%s' successfully." %new_hostgroup_name
    tmp = zapi.run("hostgroup.getobjects", {"name":new_hostgroup_name})
    new_hostgroup_id = tmp['result'][0]['groupid'] if len(tmp['result'])>0 else None  #require to create host/template
    Templates_hostgroup_name = "Templates"
    tmp = zapi.run("hostgroup.getobjects", {"name":Templates_hostgroup_name})
    Templates_hostgroup_id = tmp['result'][0]['groupid'] if len(tmp['result'])>0 else None

    #create a template "Template RAID for group Physical Machine"  [require: hostgroup_id]
    new_template_name = "Template RAID for hostgroup Physical Machine"
    tmp = zapi.run("template.exists", {"name":new_template_name})
    if tmp['result'] == False:
        zapi.run("template.create", {"host":new_template_name, "groups":{"groupid":Templates_hostgroup_id}})
        print "create template '%s' successfully." %new_template_name
    tmp = zapi.run("template.getobjects", {"host":new_template_name})
    new_template_id = tmp['result'][0]['templateid'] if len(tmp['result'])>0 else None  #require to create host/item
    #template_os_linux
    template_os_linux = "Template OS Linux"
    tmp = zapi.run("template.getobjects", {"host":template_os_linux})
    template_id_os_linux = tmp['result'][0]['templateid'] if len(tmp['result'])>0 else None

    #create any hosts and items  [require:hostgroup_id, template_id]
    new_hosts = {"test2":"192.168.110.2",
                 "test8":"192.168.110.8",
                 "test5":"192.168.110.5",
                 "test6":"192.168.110.6",
                 "test7":"192.168.110.7",
                 "os1.office.ketong.com":"192.168.200.1",
                 "os2.office.ketong.com":"192.168.200.2",
                 "os3.office.ketong.com":"192.168.200.3",
    }
    for (k, v) in new_hosts.items():
        #create a host
        tmp = zapi.run("host.exists", {"host":k})
        if tmp['result'] == False:
            zapi.run("host.create", {"host":k, 
                                     "interfaces":[{"type":1,"main":1,"useip":1,"ip":v,"dns": "","port": "10050"}],
                                     "groups":[{"groupid":new_hostgroup_id}],
#                                     "templates":[{"templateid":new_template_id},
#                                                  {"templateid":template_id_os_linux}],
                                      "templates":[{"templateid":new_template_id}],
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
        #item_1
        new_item['name'] = "Raid.info"
        new_item['key_'] = "Raid.info"
        tmp = zapi.run("item.exists", {"hostid":new_item['hostid'], "key_":new_item['key_']})
        if tmp['result'] == False:
            zapi.run("item.create", new_item)
            print "create (key:%s) of (template:%s) successfully." %(new_item['key_'], new_template_name)
        #item_2
        new_item['name'] = "Raid.disk.error"
        new_item['key_'] = "Raid.disk.error"
        tmp = zapi.run("item.exists", {"hostid":new_item['hostid'], "key_":new_item['key_']})
        if tmp['result'] == False:
            zapi.run("item.create", new_item)
            print "create (key:%s) of (template:%s) successfully." %(new_item['key_'], new_template_name)
        #item_3
        new_item['name'] = "Raid.Error_Count"
        new_item['key_'] = "Raid.Error_Count"
        tmp = zapi.run("item.exists", {"hostid":new_item['hostid'], "key_":new_item['key_']})
        if tmp['result'] == False:
            zapi.run("item.create", new_item)
            print "create (key:%s) of (template:%s) successfully." %(new_item['key_'], new_template_name)

    #create any triggers
    triggers= {}
    #trigger_1
    trigger_description = "Raid.disk.error on {HOST.NAME}"
    trigger_expression = "{%s:Raid.disk.error.abschange(0)}#0" %new_template_name
    triggers[trigger_description] = trigger_expression
    #trigger_2
    trigger_description = "Raid.Error_Count on {HOST.NAME}"
    trigger_expression = "{%s:Raid.Error_Count.abschange(0)}#0" %new_template_name
    triggers[trigger_description] = trigger_expression
    for (k,v) in triggers.items():
        tmp = zapi.run("trigger.exists", {"expression": v,
                                          "hostid": new_template_id})
        if tmp['result'] == False:
            zapi.run("trigger.create", {"description":k,
                                        "expression":v})
            print "create trigger '%s' successfully." %v

    #create action
    new_action_name = "raid1"
    tmp = zapi.run("action.exists", {"name":new_action_name})
    if tmp['result'] == False:
        zapi.run("action.create", {"name":new_action_name,
                                        "eventsource": 0,
                                        "evaltype": 0,
                                        "status": 0,
                                        "esc_period": 60,
                                        "def_shortdata": "{TRIGGER.NAME}: {TRIGGER.STATUS}",
                                        "def_longdata": "Trigger: {TRIGGER.NAME}\r\nTrigger status: {TRIGGER.STATUS}\r\nTrigger severity: {TRIGGER.SEVERITY}\r\nTrigger URL: {TRIGGER.URL}\r\n\r\nItem values:\r\n\r\n1. {ITEM.NAME1} ({HOST.NAME1}:{ITEM.KEY1}): {ITEM.VALUE1}\r\n2. {ITEM.NAME2} ({HOST.NAME2}:{ITEM.KEY2}): {ITEM.VALUE2}\r\n3. {ITEM.NAME3} ({HOST.NAME3}:{ITEM.KEY3}): {ITEM.VALUE3}\r\n\r\nOriginal event ID: {EVENT.ID}",
                                        "conditions":[
                                            {
                                            "conditiontype": 13,
                                            "operator": 0,
                                            "value": new_template_id
                                            }
                                        ],
                                        "operations":[
                                            {
                                            "operationtype": 0,
                                            "esc_period": 0,
                                            "esc_step_from": 1,
                                            "esc_step_to": 2,
                                            "evaltype": 0,
                                            "opmessage_grp":[
                                                {
                                                "usrgrpid": user_groupid_of_admin
                                                }
                                            ],
                                            "opmessage_usr":[
                                                {
                                                "userid": new_user_id
                                                }
                                            ],
                                            "opmessage":
                                                {
                                                "default_msg": 1,
                                                "mediatypeid": 1
                                                }
                                            }
                                        ]
                    }
        )
        print "create action '%s' successfully." %new_action_name

"""
result:
# python zabbix_demo.py
create hostgroup 'Physical Machine' successfully.
create template 'Template RAID for hostgroup Physical Machine' successfully.
create host successfully. (hostname:os1.office.ketong.com, ip:192.168.200.1)
create (key:Raid.info) of (template:Template RAID for hostgroup Physical Machine) successfully.
create (key:Raid.disk.error) of (template:Template RAID for hostgroup Physical Machine) successfully.
create (key:Raid.Error_Count) of (template:Template RAID for hostgroup Physical Machine) successfully.
create host successfully. (hostname:test2, ip:192.168.110.2)
create host successfully. (hostname:test5, ip:192.168.110.5)
create host successfully. (hostname:test7, ip:192.168.110.7)
create host successfully. (hostname:test6, ip:192.168.110.6)
create host successfully. (hostname:test8, ip:192.168.110.8)
create host successfully. (hostname:os2.office.ketong.com, ip:192.168.200.2)
create host successfully. (hostname:os3.office.ketong.com, ip:192.168.200.3)
create trigger '{Template RAID for hostgroup Physical Machine:Raid.disk.error.abschange(0)}#0' successfully.
create trigger '{Template RAID for hostgroup Physical Machine:Raid.Error_Count.abschange(0)}#0' successfully.
create action 'raid1' successfully.
"""
