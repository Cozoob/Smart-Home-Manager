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
    is_open = True

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
            # print(f"Received `{m}` from `{msg.topic}` topic")

            if m == "False":
                self.is_open = False
            else:
                self.is_open = True

        topic = self.sender_topic + "/open"
        client.subscribe(topic)
        client.on_message = on_message

    def _get_random_data(self) -> dict:
        # average usage of gas per minute is 0.5 kwh
        # then I assume that per 5 seconds usage is
        # between 300 kws and 420 kws
        data = dict()
        if self.is_open:
            gas_value = randint(300, 420)
        else:
            gas_value = 0
        data["gas_value"] = gas_value
        data["open"] = self.is_open
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
            # print(f"Received `{m}` from `{msg.topic}` topic")

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


class Lock(Sensor):
    open = True

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
            # print(f"Received `{m}` from `{msg.topic}` topic")

            if m == "False":
                self.open = False
            else:
                self.open = True

        topic = self.sender_topic + "/open"
        client.subscribe(topic)
        client.on_message = on_message

    def _get_random_data(self) -> dict:
        data = dict()
        data["open"] = self.open
        return data


class GasDetector(Sensor):
    is_gas_detected = True

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
        # Cannot modify state of gas detection
        ...

    def _get_random_data(self) -> dict:
        data = dict()
        self.is_gas_detected = bool(randint(1, 100) > 2)
        data["gas_detected"] = self.is_gas_detected
        return data


class Light(Sensor):
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
            # print(f"Received `{m}` from `{msg.topic}` topic")

            if m == "False":
                self.is_turn_on = False
            else:
                self.is_turn_on = True

        topic = self.sender_topic + "/turn_on"
        client.subscribe(topic)
        client.on_message = on_message

    def _get_random_data(self) -> dict:
        # brightness [%]
        # color_temperature in [coolest, cool, neutral, warm, warmest]
        color_temperatures = ["coolest", "cool", "neutral", "warm", "warmest"]

        data = dict()
        if self.is_turn_on:
            brightness_value = randint(0, 100)
            color_value = color_temperatures[randint(0, len(color_temperatures) - 1)]
        else:
            brightness_value = randint(0, 100)
            color_value = "coolest"

        data["brightness_value"] = brightness_value
        data["color_value"] = color_value
        data["turn_on"] = self.is_turn_on
        return data


class TemperatureSensor(Sensor):
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
        # Cannot change state of temperature
        ...

    def _get_random_data(self) -> dict:
        # return average temperature in household [celsius scale]
        # between 18-24
        data = dict()
        data["temperature"] = randint(18, 24)
        return data


class HumidSensor(Sensor):
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
        # Cannot change state of humidity
        ...

    def _get_random_data(self) -> dict:
        # return average humidity in household:
        # between 30-60
        data = dict()
        data["humid"] = randint(30, 60)
        return data


class RollerShade(Sensor):
    topic = ""
    is_open = True
    open_value = 100

    def __init__(self, broker: str, port: int, sender_topic: str, client_id: str):
        super().__init__(broker, port, sender_topic, client_id)

    def publish(self, data: dict):
        self.topic = self.sender_topic + "/open"
        self.subscribe(self.client)
        self.topic = self.sender_topic + "/open_value"
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
                self.open = False
                self.open_value = 0
            elif m == "True":
                self.open = True
            else:
                self.open_value = int(m)
                self.is_open = self.open_value > 0

        client.subscribe(self.topic)
        client.on_message = on_message

    def _get_random_data(self) -> dict:
        data = dict()
        data["open"] = self.is_open
        data["open_value"] = self.open_value
        return data


class GarageDoor(Sensor):
    is_open = True

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

            print(m)
            if m == "False":
                self.is_open = False
            else:
                self.is_open = True

        client.subscribe(self.sender_topic + "/open")
        client.on_message = on_message

    def _get_random_data(self) -> dict:
        data = dict()
        data["open"] = self.is_open
        return data
