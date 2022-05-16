# Smart Home Manager

## Description

[GIF]

The program is a control panel for sensors in Smart Home. The sensors are connected with the program through MQTT Broker.

The project contains also sensors' sciripts written in Python.
  
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

`make`

## Authors
- *Marcin "Cozoob" Kozub*
- *Rafał "rafibz007" Kamiński*
