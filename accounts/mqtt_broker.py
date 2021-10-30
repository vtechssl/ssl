import paho.mqtt.client as mqtt
import json
import requests
from collections import deque 

# import django
# django.setup()

# from .routes import postdata 

messages = deque()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe('test')
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    # Do something
    messages.append(str(msg.payload.decode()))
    p = 0
    # print(f'{message}')
    # print(len(messages))
    if len(messages) == 1 and p == 0:
        dat = ''.join(messages)
        print(dat)
        messages.clear()
        headers = { 'Content-Type': 'application/x-www-form-urlencoded', 'Host': '0.0.0.0', 'User-Agent': 'MQTTClient', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        requests.post(url='http://localhost:8000/post-data', data = dat,headers=headers)
        p = 1

    # message = json.loads(message)
    # print(f'{message}')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# print('message = '+message)

client.connect("13.235.16.132", 1883)