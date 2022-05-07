import time
from threading import Thread

from kivy.clock import Clock
from paho.mqtt import client as mqtt_client
import random
import json

from Sensors.connectors import MQTTConnector

BROKER = "127.0.0.1"
PORT = 1883
topic = "/haha"
client_id = f"python-mqtt-{random.randint(0, 1000)}"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connect to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set connecting Client ID
    client = mqtt_client.Client(client_id=client_id)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        print("WHAT")
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        m = json.loads(msg.payload.decode('utf-8'))
        for key in m:
            print(f"Received `{m[key]}` of key `{key}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


if __name__ == '__main__':

    # SUBSCRIBE
    connector = MQTTConnector(BROKER, PORT)
    time.sleep(0.5)
    # connector.subscribe("sensor-1/power_value")
    while True:
        time.sleep(5)
        connector.publish("sensor-0/open", False)
        time.sleep(10)
        # connector.publish("sensor-0/open", True)
        # time.sleep(10)
