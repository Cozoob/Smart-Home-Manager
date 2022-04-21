# Version of python
PYTHON=python3
# Defines the default target that 'make' will try to make.
# This target is executed whenever we just type 'make'
.DEFAULT_GOAL=help

help:
    @echo "------------------HELP------------------"
    @echo "To setup the project type 'make setup'"
    @echo "To run the project type 'make run'"
    @echo "----------------------------------------"

setup:
    @echo "Installing packages..."
    pip install -r requirements.txt
    @echo "Installing external modules for kivy..."
    # TODO Add external modules for kivy...
    @echo "Setup has been finished :)"

run:
    ${PYTHON} main.pyp