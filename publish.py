import random
import json

from paho.mqtt import client as mqtt_client

from get_config import *

emqx_config_list = get_emqx_config()
broker = emqx_config_list['broker']
port = emqx_config_list['port']
username = emqx_config_list['username']
password = emqx_config_list['password']
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect():
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker, port)
    return client

def publish_to_ceiling(status, device_mac):
    client = connect()
    topic = '/Agriculture/Controll/Ceiling'
    data = {
        "status": status,
        "device_mac": device_mac
    }
    json_msg = json.dumps(data)
    result = client.publish(topic, json_msg)
    result_type = result[0]
    if result_type == 0:
        print(f'send "{json_msg} to topic "{topic}""')
    else:
        print(f'failed to send message to topic "{topic}"')

def publish_to_fan(status, device_mac):
    client = connect()
    topic = '/Agriculture/Controll/Fan'
    data = {
        "status": status,
        "device_mac": device_mac
    }
    json_msg = json.dumps(data)
    result = client.publish(topic, json_msg)
    result_type = result[0]
    if result_type == 0:
        print(f'send "{json_msg} to topic "{topic}""')
    else:
        print(f'failed to send message to topic "{topic}"')

def publish_to_curtain(status, device_mac):
    client = connect()
    topic = '/Agriculture/Controll/Curtain'
    data = {
        "status": status,
        "device_mac": device_mac
    }
    json_msg = json.dumps(data)
    result = client.publish(topic, json_msg)
    result_type = result[0]
    if result_type == 0:
        print(f'send "{json_msg} to topic "{topic}""')
    else:
        print(f'failed to send message to topic "{topic}"')

if __name__ == '__main__':
    status = int(input('请输入状态：'))
    device_mac = input('请输入设备mac：')
    publish_to_curtain(status, device_mac)
