from paho.mqtt import client as mqtt_client
from time import sleep
from random import randint

from abc import ABC, abstractmethod


class Sensor(ABC):
    def __init__(self, broker: str, port: int, sender_topic: str, client_id: str):
        self.sender_topic = sender_topic
        self.port = port
        self.client_id = client_id
        self.broker = broker
        self.client = self.__connect_mqtt()

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

    def _check_status(self, status: int):
        if status != 0:
            print(f"Failed to send message to topic {self.sender_topic}")

    @abstractmethod
    def publish(self, data: dict):
        ...

    @abstractmethod
    def subscribe(self, client: mqtt_client):
        ...

    @abstractmethod
    def _get_random_data(self) -> dict:
        ...


class GasValveSensor(Sensor):
    is_turn_on = True

    def __init__(self, broker: str, port: int, sender_topic: str, client_id: str):
        super().__init__(broker, port, sender_topic, client_id)

    def publish(self, data: dict):
        self.subscribe(self.client)
        self.client.loop_start()
        while True:
            random_data = self._get_random_data()
            for key in random_data:
                result = self.client.publish(
                    self.sender_topic + "/" + key, random_data[key]
                )
                status = result[0]
                self._check_status(status)
            sleep(5)

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            m = msg.payload.decode("utf-8")
            print(f"Received `{m}` from `{msg.topic}` topic")

            if m == "False":
                self.is_turn_on = False
            else:
                self.is_turn_on = True

        topic = self.sender_topic + "/turn_on"
        client.subscribe(topic)
        client.on_message = on_message

    def _get_random_data(self) -> dict:
        # average usage of gas per minute is 0.5 kwh
        # then I assume that per 5 seconds usage is
        # between 300 kws and 420 kws
        data = dict()
        if self.is_turn_on:
            gas_value = randint(300, 420)
        else:
            gas_value = 0
        data["gas_value"] = gas_value
        data["turn_on"] = self.is_turn_on
        return data


class SmartPlug(Sensor):
    is_turn_on = True

    def __init__(self, broker: str, port: int, sender_topic: str, client_id: str):
        super().__init__(broker, port, sender_topic, client_id)

    def publish(self, data: dict):
        self.subscribe(self.client)
        self.client.loop_start()
        while True:
            random_data = self._get_random_data()
            for key in random_data:
                result = self.client.publish(
                    self.sender_topic + "/" + key, random_data[key]
                )
                status = result[0]
                self._check_status(status)
            sleep(5)

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            m = msg.payload.decode("utf-8")
            print(f"Received `{m}` from `{msg.topic}` topic")

            if m == "False":
                self.is_turn_on = False
            else:
                self.is_turn_on = True

        topic = self.sender_topic + "/turn_on"
        client.subscribe(topic)
        client.on_message = on_message

    def _get_random_data(self) -> dict:
        # average usage of gas per minute is 5 kwh
        # then I assume that per 5 seconds usage is
        # between 3000 kws and 4200 kws
        data = dict()
        if self.is_turn_on:
            power_value = randint(3000, 4200)
        else:
            power_value = 0
        data["power_value"] = power_value
        data["turn_on"] = self.is_turn_on
        return data
