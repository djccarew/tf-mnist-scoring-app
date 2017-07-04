##
#  Copyright 2017 IBM Corp. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#  https://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
##
# Functions to get/put binary files from/to Bluemix Object Storage
#
import requests  
import json  

class TokenException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
        
class SwiftPUTException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
        
class SwiftGETException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

        
def get_binary_file(credentials, container, remote_file_name, local_file_path):  
    """
    This function creates a local file from file
    content retrieved from Bluemix Object Storage V3.
    
    Parameters:
       credentials - a dictionary containing access credentials to an instance of Bluemix Object Storage
                     Dictionary keys are expected to be the same as the JSON field names  in 
                     the service credentials 
       container - the name of the  container contains the file to be fetched
       remote_file_name - the name of the file in Object Storage
       local_file_path - the full path of the local file that will be created
    """
    try: 
       f = open(local_file_path,'w+')
    except IOError:
        print("get_binary_file: Could not open file", local_file_path)
        return
    
    url1 = ''.join([credentials["auth_url"], '/v3/auth/tokens'])
    data = {"auth": {"identity": {"methods": ["password"],
            "password": { "user": {"id": credentials["user_id"],
             "password": credentials["password"]}}},
            "scope": { "project": {"id": credentials["project_id"]}}}}	
    headers1 = {'Content-Type': 'application/json'}
    resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
    print(resp1)
    if resp1.status_code != 201:
        raise TokenException("status_code " + str(resp1.status_code))
        
    resp1_body = resp1.json()
    for e1 in resp1_body['token']['catalog']:
        if(e1['type']=='object-store'):
            for e2 in e1['endpoints']:
                        if(e2['interface']=='public'and e2['region']==credentials['region']):
                            url2 = ''.join([e2['url'],'/', container, '/', remote_file_name])
    s_subject_token = resp1.headers['x-subject-token']
    headers2 = {'X-Auth-Token': s_subject_token}
    resp2 = requests.get(url=url2, headers=headers2 )
    if resp2.status_code == 200:
       try:
          f.write(resp2.content)
       except IOError:
          print("get_binary_file: Could not write to file", local_file_path)
          return
    else:
       raise SwiftGETException("status_code " +  str(resp2.status_code))
        
    f.close()
    print (resp2)
    return
    
def put_binary_file(credentials, container, remote_file_name, local_file_path):  
    """
    This function creates a file in Bluemix
    Object Storage V3 from a local file.
       
    Parameters:
       credentials - a dictionary containing access credentials to an instance of Bluemix Object Storage
                     Dictionary keys are expected to be the same as the JSON field names  in 
                     the service credentials 
       container - the name of the  container the contains the file to be created
       remote_file_name - the name of the file to be created in Object Storage
       local_file_path - the full path of the local source file
    """
    
    try:
       f = open(local_file_name,'rb')
       my_data = f.read()
    except IOError:
        print("put_binary_file: Could not open file", local_file_path)
        return 
        
    
    url1 = ''.join([credentials["auth_url"], '/v3/auth/tokens'])
    data = {"auth": {"identity": {"methods": ["password"],
            "password": { "user": {"id": credentials["user_id"],
             "password": credentials["password"]}}},
            "scope": { "project": {"id": credentials["project_id"]}}}}	
    headers1 = {'Content-Type': 'application/json'}
    resp1 = requests.post(url=url1, data=json.dumps(data), headers=headers1)
    print(resp1)
    if resp1.status_code != 201:
       raise TokenException("status_code " +  str(resp1.status_code))
        
    resp1_body = resp1.json()
    for e1 in resp1_body['token']['catalog']:
        if(e1['type']=='object-store'):
            for e2 in e1['endpoints']:
                        if(e2['interface']=='public'and e2['region']==credentials['region']):
                            url2 = ''.join([e2['url'],'/', container, '/', remote_file_name])
    s_subject_token = resp1.headers['x-subject-token']
    headers2 = {'X-Auth-Token': s_subject_token, 'accept': 'application/json'}
    resp2 = requests.put(url=url2, headers=headers2, data = my_data )
    if resp2.status_code != 201:
       raise SwiftPUTException("status_code " +  str(resp2.status_code))    
    print (resp2)
    return