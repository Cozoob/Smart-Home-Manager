from enum import Enum, auto


class SensorType(Enum):
    GAS_VALVE = auto()
    SMART_PLUG = auto()
    LOCKER = auto()
    GAS_DETECTOR = auto()
    LIGHT = auto()
    TEMPERATURE = auto()
    HUMID = auto()
    ROLLER_SHADE = auto()
    GARAGE_DOOR = auto()
    OTHER = auto()


class ColorTemperature(Enum):
    COOLEST = auto()
    COOL = auto()
    NEUTRAL = auto()
    WARM = auto()
    WARMEST = auto()
