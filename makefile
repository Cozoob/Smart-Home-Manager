# Version of python
PYTHON=python3
# Defines the default target that 'make' will try to make.
# This target is executed whenever we just type 'make'
.DEFAULT_GOAL=help

help:
	@echo "------------------HELP------------------"
	@echo "To run the project type 'make run'"
	@echo "Make sure that mqtt broker is running"
	@echo "----------------------------------------"

run:
	cd ControlPanel; ${PYTHON} main.py &
	cd SensorScripts; ${PYTHON} main.py
