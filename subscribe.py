import random
import json

from paho.mqtt import client as mqtt_client
from db_utils import *

from get_config import *

mysql_config_list = get_mysql_config()
emqx_config_list = get_emqx_config()

broker = emqx_config_list['broker']
port = emqx_config_list['port']
db_user_name = mysql_config_list['username']
db_user_password = mysql_config_list['password']
db_name = mysql_config_list['database']
client_id = f'subscribe-{random.randint(0,100)}'
emqx_user_name = emqx_config_list['username']
emqx_user_password = emqx_config_list['password']
topic = emqx_config_list['topic']

def connect_mysql():
    try:
        db, cursor = connect(broker, db_user_name, db_user_password, db_name)
        return db, cursor
    except Exception as e:
        print(f'in connect_mysql,catch err:{e}')
        
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to MQTT Broker!\n')
        else:
            print(f'Failed to connect,return code {rc}\n')
    
    client = mqtt_client.Client(client_id)
    client.username_pw_set(emqx_user_name, emqx_user_password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(db, cursor, client: mqtt_client):
    def on_message(client, userdata, message):
        topic1 = message.topic
        print(topic1)

        topic_split = topic1.split('/')
        print(topic_split)

        if len(topic_split) < 3:
            print("Invalid topic format")
            return

        if topic_split[2] not in ['Air', 'Soil']:
            print(f"Invalid topic type: {topic_split[2]}")
            return

        print(f"topic_split[1]: {topic_split[1]}, topic_split[2]: {topic_split[2]}")

        try:
            msg_str = message.payload.decode('utf-8')
            msg_json = json.loads(msg_str)
            # print(f"msg_json:{msg_json}")
        except json.JSONDecodeError:
            print("Invalid JSON format in message payload")
            return

        mac = msg_json.get('MAC', '')
        if not mac:
            print("MAC address is missing or empty")
            return

        if topic_split[2] == 'Air':
            params = msg_json.get('params', {})
            # print(f"params:{params}")
            air_temp = params.get('air_temp', '')
            air_humid = params.get('air_humid', '')

            if not air_temp or not air_humid:
                print("Air temperature or humidity is missing")
                return

            insertVal = {
                'air_temp': air_temp,
                'air_humid': air_humid,
                'device_mac': mac
            }

            insert(db, cursor, 'air',insertVal)
        elif topic_split[2] == 'Soil':
            params = msg_json.get('params', {})
            moisture_value = params.get('moisture_value', '')
            temperature_value = params.get('temperature_value', '')
            conductivity_value = params.get('conductivity_value', '')
            pH_value = params.get('pH_value', '')
            nitrogen = params.get('nitrogen', '')
            phosphorus = params.get('phosphorus', '')
            potassium = params.get('potassium', '')
            
            if not all([moisture_value, temperature_value, conductivity_value, pH_value, nitrogen, phosphorus, potassium, device_mac]):
                print("Some required soil parameters are missing")
                return

            insertVal = {
                    'moisture_value': moisture_value,
                    'temperature_value': temperature_value,
                    'conductivity_value': conductivity_value,
                    'pH_value': pH_value,
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium,
                    'device_mac': mac
            }

            insert(db, cursor, 'soil',insertVal)
        
    client.subscribe(topic)
    client.on_message = on_message

def run():
    try:
        db, cursor = connect_mysql()
        client = connect_mqtt()
        subscribe(db, cursor, client)
        client.loop_forever()
    except Exception as e:
        print(f'catch err:{e}')

if __name__=='__main__':
    run()
