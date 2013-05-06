from zabbix_api import ZabbixAPI
import sys

try:
    location = sys.argv[1]
except:
    print "python zabbix_item_add.py location(112,114,bgp,center,telcom,unicom)"
    exit(1)

if location == '112':
    server = "http://192.168.1.112/zabbix"
    username = "admin"
    password = "zabbix"
elif location == '114':
    server = "http://192.168.1.114/zabbix"
    username = "admin"
    password = "zabbix"
else:
    print "python zabbix_item_add.py location(bgp,center,telcom,unicom)"
    exit(1)

zapi = ZabbixAPI(server=server, path="")
zapi.login(username, password)

host_name = "test"
#host_name = "Zabbix server"
template_name = "Template OS Linux"
#template_name = "Template App Zabbix Server"
hostgroup = "Linux servers"
#hostgroup = "Zabbix servers"
template_id=zapi.template.get({"filter":{"host":template_name}})[0]["templateid"]

template_item_key = 'net.tcp.listen[22]'
#items=zapi.item.exists({"host":host_name,"key_": template_item_key})
items=zapi.item.exists({"key_": template_item_key})
if items == False:
    print '### Begin to Create an item: '+template_item_key
    result = zapi.item.create({ 'hostid' : (template_id), 'key_': template_item_key, 'name':tem
plate_item_key, 'type':0, 'value_type':3, 'data_type':3,'delay':60, 'trends':21,'history':7})
else:
    print '### The item is already in the template, Do nothing.'
