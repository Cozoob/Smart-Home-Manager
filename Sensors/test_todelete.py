# Created by Marcin "Cozoob" Kozub 07.05.2022
import time

from sensors import Light

if __name__ == '__main__':
    BROKER = "127.0.0.1"
    PORT = 8080
    sensor = Light("sensor-0", BROKER, PORT)
    print(sensor.get_sensor_type())

    i = 0
    while i < 100:
        print(sensor.get_is_turn_on())
        time.sleep(3)
        sensor.turn_off()
        i += 1

    sensor.disconnect()
