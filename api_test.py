#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
test openstack-ceilometer-api
@author: wangyucheng
mod={'post':   "create",
     'get':    "list",
     'delete': "delete",
     'put':    "update"
}
"""

import json
import urllib2
import sys

class TestApi:
    def __init__(self):
        self.auth_post = {"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "09c2551a446f47c3"}}}
        self.auth_url  = "http://10.179.203.5:5000/v2.0/tokens"
        self.api_url1  = "http://10.179.203.5:8777/v2/groups"
        self.api_url2  = "http://10.179.203.5:8777/v2/emails"
        self.api_url3  = "http://10.179.203.5:8777/v2/snss"
        self.api_url4  = "http://10.179.203.5:8777/v2/email/4aec01ef-95b5-4e1b-8e8c-09e402a83bbe"
        self.header    = {"Content-Type": "application/json",
                           "Accept": "application/json"
        }
    def _set_auth_session(self):
        self.header['User-Agent'] = "python-keystoneclient"
        response = self._request(self.auth_url, self.auth_post)
        user_id = response['access']['user']['id']
        token_id = response['access']['token']['id']
        return user_id,token_id

    def _request(self,url, data=None, mod=None):
        if data is not None:
            post_data = json.dumps(data)
            #print post_data
            req = urllib2.Request(url,post_data)
        else:
            req = urllib2.Request(url)
        for k,v in self.header.items():
            req.add_header(k,v)
        if mod is not None:
            req.get_method = lambda:mod
        try:
            result = urllib2.urlopen(req)
        except urllib2.URLError as e:
            print e.code
        else:
            response = json.loads(result.read())
            result.close()
            return response

    def run1(self):
        user_id, token_id = self._set_auth_session()
        self.header['User-Agent'] = "python-ceilometerclient"
        self.header['X-Auth-Token'] = token_id
        ##get all
        response = self._request(self.api_url1, mod='GET')
        ##get one
        #response = self._request("http://10.179.203.5:8777/v2/groups/fc79338a-b24e-4a04-8047-83e419373d39", mod='GET')
        ##post
        #response = self._request(self.api_url1, {"group_name":"wyc"}, mod='POST') 
        ##delete
        #response = self._request("http://10.179.203.5:8777/v2/groups/dad43740-2284-4541-b3e6-045ea57ce054", mod='DELETE')
        ##put
        #response = self._request("http://10.179.203.5:8777/v2/groups/df48c470-d964-435a-8b7c-944c92c95ebb", {"group_name":"xxx"}, mod='PUT')
        if response:
            print response

    def run2(self):
        user_id, token_id = self._set_auth_session()
        self.header['User-Agent'] = "python-ceilometerclient"
        self.header['X-Auth-Token'] = token_id
        ##post
        #response = self._request(self.api_url2, {"email_desc":"this is a test","email_addr":"wangyucheng13@qq.com","group_uuid":"cd4e725b-03ff-4f6b-978a-e5cdef3313af"}) 
        ##get
        response = self._request("http://10.179.203.5:8777/v2/email/007e0cf5-c4d9-43c6-8f09-46ee869ce419", mod='GET') 
        ##delete
        #response = self._request("http://10.179.203.5:8777/v2/email/4d7420ba-799b-4bc8-b5bb-06081eaf3084", mod='DELETE')
        ##put
        #response = self._request("http://10.179.203.5:8777/v2/email/007e0cf5-c4d9-43c6-8f09-46ee869ce419", {"email_addr":"wyc@163.com"}, mod='PUT')
        if response:
            print response

    def run3(self):
        user_id, token_id = self._set_auth_session()
        self.header['User-Agent'] = "python-ceilometerclient"
        self.header['X-Auth-Token'] = token_id
        ##post
        #response = self._request(self.api_url3, {"sns_desc":"this is a test3","sns_phone":"113123322","group_uuid":"cd4e725b-03ff-4f6b-978a-e5cdef3313af"}) 
        ##get all
        response = self._request("http://10.179.203.5:8777/v2/snss/cd4e725b-03ff-4f6b-978a-e5cdef3313af", mod='GET') 
        ##get one
        #response = self._request("http://10.179.203.5:8777/v2/sns/877e74d7-edfa-438a-a25a-706a529563d6", mod='GET')
        ##put
        #response = self._request("http://10.179.203.5:8777/v2/sns/e6d925ac-07f5-4008-acb5-3f8d43647eec", {"sns_phone":'111',"sns_desc":'222'}, mod='PUT')
        if response:
            print response


if __name__ == "__main__":
    client = TestApi()
    client.run1()
