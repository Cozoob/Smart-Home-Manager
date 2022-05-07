# Created by Marcin "Cozoob" Kozub 07.05.2022
import time

from sensors import TemperatureSensor

if __name__ == '__main__':
    BROKER = "127.0.0.1"
    PORT = 1883
    sensor = TemperatureSensor("sensor-0", BROKER, PORT)
    print(sensor.get_sensor_type())

    i = 0
    while i < 10:
        print(sensor.get_temperature())
        time.sleep(2)
        i += 1

    sensor.disconnect()
