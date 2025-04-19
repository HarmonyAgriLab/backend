import random
import time

from paho.mqtt import client as mqtt_client

from get_config import *

emqx_config_list = get_emqx_config()
broker = emqx_config_list['broker']
port = emqx_config_list['port']
username = emqx_config_list['username']
password = emqx_config_list['password']
topic = '/python/test'
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def publish():
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker, port)
    msg_count = 0
    while msg_count < 5:
        time.sleep(1)
        msg = f'messages: {msg_count}'
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f'send "{msg}" to topic "{topic}"')
        else:
            print(f'failed to send message to topic "{topic}"')
        msg_count += 1

if __name__ == '__main__':
    publish()
