from abc import ABC
from typing import Tuple

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.layout import Layout

from GUI.Sensors.scheme_object import SchemeSensor


class SchemeLightSensor(SchemeSensor):
    def set_unavailable_state(self): ...
    def set_available_state(self): ...

    MAIN_IMAGE = "./Resources/SensorIcons/light-bulb-icon.jpg"
    SENSOR_NAME = "AduroSmartLight"

    def __init__(self, sensor=None, **kwargs):
        super(SchemeLightSensor, self).__init__(self.SENSOR_NAME, **kwargs)
        self.sensor = sensor

        super()._set_background_image(self.MAIN_IMAGE)

    def get_popup_window_content(self) -> Tuple[Layout, Button]:
        main_boxlayout = BoxLayout(orientation='vertical')
        main_boxlayout.add_widget(Label(text="haha"))

        close_button = Button()

        main_boxlayout.add_widget(close_button)
        return main_boxlayout, close_button

