#coding=utf-8
import sys


import base64
import time
from openstack import connection
from openstack import utils
#utils.enable_logging(debug=True, stream=sys.stdout)




#create connection

username = "xxxxxxxxx"
password = "xxxxxxxxxxxxxxx"
projectId = "438fe291fdc5xxxxxxxxxxxxx"
userDomainId = "7c959d14cf07xxxxxxxxxxx"
auth_url = "https://iam.cn-north-1.myhuaweicloud.com/v3"
conn = connection.Connection(auth_url=auth_url,
                             user_domain_id=userDomainId,
                             project_id=projectId,
                             username=username,
                             password=password
                            )

#set parameters
TIMES = 60
INTERVAL = 10
limit = 5
#define function for listing servers

def create_server():
    data = {
        "availability_zone": "ap-southeast-1b",
        "name":"test-api-createserver",
        "image_id":"8be4abab-1ae3-4f5e-9245-0a77f2ef4d46",
        "flavor_id":"s3.small.1",
        "adminPass":"xxxxxxxxx",
        "vpcid": "d0a98695-a46c-4406-b4a5-938c4cc5b280",
        "nics": [
            {
                 "subnet_id": "939b9cdd-eeb9-4036-b480-65b4bf9d0ebb"
            
            }
            ],
       # "extendparam":
       #     {
       #     "chargingMode":0
       #     },
        "securuty_groups":[
            {
                "id":"68e6dd8f-ab74-4657-af09-c65f2cc54fe8"
            }
        ],
        "root_volume":[
            {
                "volumetype":"SSD"
            }
        ],
    "publicip": {
        "eip": {
            "iptype": "5_bgp",
            "bandwidth":
                    {
                        "size": 5,
                        "sharetype": "PER"
                    }
           # "extendparam": {
           #      "chargingMode": "postPaid"
           # }
            }  
        },
    }
    server = conn.ecs.create_server_ext(**data)
#    print server
#    return server


def list_servers():
    #get server list with params
    servers = conn.compute.servers(limit=1)
    #iterate servers list
    for server in servers:
        print server
#list_servers()
#visit API 

def show_server(server_id):
    server = conn.compute.get_server(server_id)
    print server
    a='5b1da039-6a94-4f37-a328-13d3ef5ec1dd'
#show_server(a)
def reboot_server():
    pass

def start_server():
    data = {
        "os-start":{
            "servers":[
                {
                    "id":"13d03d0a-e9da-47f9-b6f4-3b81aa142f37"
                }
            ]
        }
    }
    ff = conn.ecs.start_server(**data)
    print ff
    wait_time(TIMES,INTERVAL,ff.job_id)


def stop_server():
    data = {
    "os-stop":{
        "type":"SOFT",
        "servers":[
            {
                "id":"13d03d0a-e9da-47f9-b6f4-3b81aa142f37"
            }
        ]
    }
    }
    ff = conn.ecs.stop_server(**data)
    print ff
    wait_time(TIMES,INTERVAL,ff.job_id)

def wait_time(times,interval,job_id):
    for index in range(times):
        time.sleep(interval)
        job = conn.ecs.get_job(job_id)
        if job.status == "SUCCESS":
            print "Get job success after %s tries" %index
            break
if __name__ == "__main__":
    print ("""
            功能菜单
            1.创建虚拟机
            2.虚拟机开机
            3.虚拟机关机
            0.退
            """
    )
    youinput = int(raw_input("Input num is:"))
    if youinput == 2:
        start_server()
    elif youinput == 3:
        stop_server()
    elif youinput == 1:
        create_server()
