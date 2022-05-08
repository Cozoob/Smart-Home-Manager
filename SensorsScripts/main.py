# Created by Marcin "Cozoob" Kozub 05.05.2022
import fnmatch
import os
import subprocess
import sys
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


def locate(pattern, root=os.curdir):
    """
    Locate dir matching supplied dirname pattern in and below
    supplied root directory.
    """
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for dirname in fnmatch.filter(dirs, pattern):
            return os.path.join(path, dirname)


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

    file = os.path.join(os.getcwd(), "sensor.py")
    pythonpath = os.environ["PYTHONPATH"]

    os.chdir("..")
    cwd = locate("site-packages")
    # print(cwd)

    process_env = os.environ.copy()
    print(process_env["PYTHONPATH"])
    # process_env["PYTHONPATH"].join(cwd)

    if pythonpath.find(";"):
        # windows
        process_env["PYTHONPATH"] = cwd + ";" + process_env["PYTHONPATH"]
    else:
        # linux
        process_env["PYTHONPATH"] = cwd + ":" + process_env["PYTHONPATH"]


    # example:
    # C:\Users\mnkoz\PycharmProjects\Smart-Home-Manager\venv\Lib\site-packages\paho
    sys.path.append(cwd)

    print(process_env["PYTHONPATH"])

    # create_subprocess(sensors.GasValveSensor.__name__)
    # create_subprocess(sensors.SmartPlug.__name__)
    # create_subprocess(sensors.Lock.__name__)
    # create_subprocess(sensors.GasDetector.__name__)
    create_subprocess(sensors.Light.__name__)
    # create_subprocess(sensors.TemperatureSensor.__name__)
    # create_subprocess(sensors.HumidSensor.__name__)
    # create_subprocess(sensors.RollerShade.__name__)
    # create_subprocess(sensors.GarageDoor.__name__)

    while True:
        pass
