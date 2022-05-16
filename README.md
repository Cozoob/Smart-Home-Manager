# Smart Home Manager

## Description

The program is a control panel for sensors in Smart Home. The sensors are connected with the program through MQTT Broker.

The project contains also sensors' sciripts written in Python.

**Sensor scripts working**

![Gif presents sensor scripts working.](https://user-images.githubusercontent.com/90906410/168673712-418dbd5a-d8a4-4b49-97b3-3557aea0b10f.gif)

**Preview control panel**

![Gif presents control panel working.](https://user-images.githubusercontent.com/90906410/168682473-c8d0670f-88f0-496b-a4c8-1143a3dcff19.gif)
  
**Interaction with sensors**

![Gif presents interaction with sensors.](https://user-images.githubusercontent.com/90906410/168682572-7bee90e8-a293-411a-80aa-bf45438b6525.gif)

**Adding new floor and a sensor - editing scheme**

![Gif presents editing scheme.](https://user-images.githubusercontent.com/90906410/168682658-a05f1ab6-7c6c-4f1c-b3e6-b3edd15a02f8.gif)
  
## Libraries
- Kivy
- PahoMQTT
  
## How to run
1. Clone this repo.

`git clone <repo>`

2. Change directory (for each: 'ControlPanel' and 'SensorScripts' do 2-6).

`cd <repo>`

3. Instal virutalenv if you don't already have virtualenv installed.

`pip install virtualenv`

4. Create your new environment.

`virtualenv venv`

5. Enter the virtual environment.

`source venv/bin/activate`

6. Install the requirements in the current environment.

`pip install -r requirements.txt`

7. Run mosquitto broker (Install mosquitto mqtt broker if you don't have it).

`mosquitto –p 1883 –v`

8. Run makefile.

`make run`

## Authors
- *Marcin "Cozoob" Kozub*
- *Rafał "rafibz007" Kamiński*
