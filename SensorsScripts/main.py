# Created by Marcin "Cozoob" Kozub 05.05.2022
import os
import subprocess
import time

import sensors
import signal

NAME = "sensor-"
COUNTER = 0

BROKER = "127.0.0.1"
PORT = 1883

CHILDREN = []


def signal_handler(signum, frame):
    print("Killing all children!")
    for child in CHILDREN:
        print("pid: ", child.pid)
        child.terminate()
        time.sleep(1)
        print("status: ", child.poll())

    print("Exit the program in 3 seconds...")
    time.sleep(3)
    exit(0)


def create_subprocess(class_name: str):
    global COUNTER
    p = subprocess.Popen(
        ["python3", file] + [BROKER, str(PORT), NAME, str(COUNTER), class_name, NAME],
        env=process_env,
    )
    print("Sensor child's pid: ", p.pid, " | Sensor type: ", class_name)
    CHILDREN.append(p)
    COUNTER += 1


if __name__ == "__main__":
    # handling all signals
    for i in [x for x in dir(signal) if x.startswith("SIG")]:
        try:
            signum = getattr(signal, i)
            if isinstance(signum, signal.Signals):
                signal.signal(signum, signal_handler)
        except (OSError, RuntimeError) as m:  # OSError for Python3, RuntimeError for 2
            print("Skipping {}".format(i))

    time.sleep(1)

    file = os.getcwd() + r"\sensor.py"
    pythonpath = os.environ["PYTHONPATH"]
    os.chdir("..")
    cwd = os.getcwd() + r"\venv\Lib\site-packages"
    process_env = os.environ.copy()
    # example:
    # C:\Users\mnkoz\PycharmProjects\Smart-Home-Manager\venv\Lib\site-packages\paho
    process_env["PYTHONPATH"] = cwd + ";" + process_env["PYTHONPATH"]

    # create_subprocess(sensors.GasValveSensor.__name__)
    # create_subprocess(sensors.SmartPlug.__name__)
    # create_subprocess(sensors.Lock.__name__)
    # create_subprocess(sensors.GasDetector.__name__)
    # create_subprocess(sensors.Light.__name__)
    create_subprocess(sensors.TemperatureSensor.__name__)
    # create_subprocess(sensors.HumidSensor.__name__)
    # create_subprocess(sensors.RollerShade.__name__)
    # create_subprocess(sensors.GarageDoor.__name__)

    while True:
        pass
