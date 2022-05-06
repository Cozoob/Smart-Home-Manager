import typing

from paho.mqtt import client as mqtt_client
from random import randint


class MQTTConnector:
    def __init__(self, broker: str, port: int):
        self.broker = broker
        self.port = port

        self.client_id = f"python-mqtt-{randint(0, 1000)}"
        self.client = self.__connect_mqtt()
        self.data = {}

    def set_broker(self, broker: str):
        self.broker = broker

    def set_port(self, port: int):
        self.port = port

    def publish(self, topic: str, data: typing.Any):

        msg_count = 0

        self.client.loop_start()
        self.client.publish(topic, data)

    def subscribe(self, topic: str):
        def on_message(client, userdata, msg):
            self.data = msg.payload.decode("utf-8")
            print(f"Received `{self.data}` of key from `{msg.topic}` topic")

        self.client.loop_start()
        self.client.subscribe(topic)
        self.client.on_message = on_message

    def __connect_mqtt(self) -> mqtt_client:
        def on_connect(client_id: mqtt_client, userdata, flags, rc: int):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id=self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client


class SensorConnector:
    def __init__(self, connector: MQTTConnector):
        self.connector = connector

    def send_data(self, topic: str, data: dict):
        pass

    def subscribe(self, topic: str) -> dict:
        pass

    def unsubscribe(self, topic: str):
        pass
