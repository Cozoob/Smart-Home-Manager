from abc import ABC, abstractmethod
from .connectors import MQTTConnector, SensorConnector
from .enums import SensorType, ColorTemperature
from .interfaces import Openable, Turnable


class Sensor(ABC):
    connector: SensorConnector
    sensor_id: str
    sensor_type: SensorType

    def __init__(self, sensor_id: str, broker: str, port: int):
        self.connector = SensorConnector(MQTTConnector(broker, port, sensor_id))
        self.sensor_id = sensor_id
        self.sensor_type = self.get_sensor_type()

    def get_sensor_id(self) -> str:
        return self.sensor_id

    @abstractmethod
    def get_sensor_type(self) -> SensorType:
        ...

    def set_new_connector(self, connector: SensorConnector):
        self.connector.unsubscribe_all()
        self.connector = connector

    def disconnect(self):
        self.connector.unsubscribe_all()


class TemperatureSensor(Sensor):
    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.TEMPERATURE

    def get_temperature(self) -> int:
        return int(self.connector.get_data("temperature"))


class GasDetector(Sensor):
    is_gas_detected: bool = False

    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.GAS_DETECTOR

    def check_gas_density(self) -> int:
        return int(self.connector.get_data("gas_density"))

    def get_is_gas_detected(self) -> bool:
        self.is_gas_detected = bool(self.connector.get_data("gas_detected"))
        return self.is_gas_detected


class HumidSensor(Sensor):
    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.HUMID

    def get_humid(self) -> int:
        return int(self.connector.get_data("humid"))


class RollerShade(Sensor, Openable):
    is_open: bool = False
    open_value: int = 0

    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.ROLLER_SHADE

    def open(self):
        self.is_open = True
        self.connector.send_data("open", True)

    def close(self):
        self.is_open = False
        self.connector.send_data("open", False)

    def get_is_open(self):
        self.is_open = bool(self.connector.get_data("open"))
        return self.is_open

    def get_open_value(self):
        self.open_value = int(self.connector.get_data("open_value"))
        return self.open_value

    def set_open_value(self, value: int):
        self.open_value = value
        self.connector.send_data("open_value", value)


class GasValve(Sensor, Openable):
    is_open: bool = False

    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.GAS_VALVE

    def open(self):
        self.is_open = True
        self.connector.send_data("open", True)

    def close(self):
        self.is_open = False
        self.connector.send_data("open", False)

    def get_is_open(self) -> bool:
        self.is_open = bool(self.connector.get_data("open"))
        return self.is_open

    def check_gas_value(self) -> int:
        return int(self.connector.get_data("gas_value"))


class Locker(Sensor, Openable):
    is_open: bool = False

    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.LOCKER

    def open(self):
        self.is_open = True
        self.connector.send_data("open", True)

    def close(self):
        self.is_open = False
        self.connector.send_data("open", False)

    def get_is_open(self) -> bool:
        self.is_open = bool(self.connector.get_data("open"))
        return self.is_open


class GarageDoor(Sensor, Openable):
    is_open: bool = False

    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.GARAGE_DOOR

    def open(self):
        self.is_open = True
        self.connector.send_data("open", True)

    def close(self):
        self.is_open = False
        self.connector.send_data("open", False)

    def get_is_open(self) -> bool:
        self.is_open = bool(self.connector.get_data("open"))
        return self.is_open


class Light(Sensor, Turnable):
    is_turn_on: bool = False
    brightness: int = 0
    color_temperature: ColorTemperature = ColorTemperature.COOLEST

    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.LIGHT

    def turn_on(self):
        self.connector.send_data("turn_on", True)
        self.is_turn_on = True

    def turn_off(self):
        self.connector.send_data("turn_on", False)
        self.is_turn_on = False

    def get_is_turn_on(self) -> bool:
        self.is_turn_on = bool(self.connector.get_data("turn_on"))
        return self.is_turn_on

    def get_color_temperature(self) -> ColorTemperature:
        return self.color_temperature

    def set_color_temperature(self, new_color_temperature: ColorTemperature):
        self.color_temperature = new_color_temperature
        self.connector.send_data("color_value", str(self.color_temperature.value))

    def get_brightness(self) -> int:
        self.brightness = int(self.connector.get_data("brightness_value"))
        return self.brightness

    def set_brightness(self, value: int):
        self.brightness = value
        self.connector.send_data("brightness_value", value)


class SmartPlug(Sensor, Turnable):
    is_turn_on: bool = False
    power_value: int = 0

    def __init__(self, sensor_id: str, broker: str, port: int):
        super().__init__(sensor_id, broker, port)

    def get_sensor_type(self) -> SensorType:
        return SensorType.SMART_PLUG

    def turn_on(self):
        self.connector.send_data("turn_on", True)
        self.is_turn_on = True

    def turn_off(self):
        self.connector.send_data("turn_on", False)
        self.is_turn_on = False

    def get_is_turn_on(self) -> bool:
        self.is_turn_on = bool(self.connector.get_data("turn_on"))
        return self.is_turn_on

    def get_power_value(self) -> int:
        self.power_value = int(self.connector.get_data("power_value"))
        return self.power_value
