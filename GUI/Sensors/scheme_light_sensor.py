from abc import ABC
from typing import Tuple

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.layout import Layout

from GUI.Sensors.PopUpWindowUtils.popup_readonly_field import ReadOnlyField
from GUI.Sensors.PopUpWindowUtils.popup_readwrite_field import ReadWriteField
from GUI.Sensors.scheme_object import SchemeSensor


class SchemeLightSensor(SchemeSensor):
    # def set_unavailable_state(self): ...
    # def set_available_state(self): ...

    MAIN_IMAGE = "./Resources/SensorIcons/light-bulb-icon.jpg"
    SENSOR_NAME = "AduroSmartLight"

    def __init__(self, **kwargs):
        super(SchemeLightSensor, self).__init__(self.SENSOR_NAME, **kwargs)
        # self.sensor = sensor

        super().set_background_image(self.MAIN_IMAGE)

    def get_popup_window_content(self) -> Tuple[Layout, Button]:
        main_boxlayout = BoxLayout(orientation='vertical')

        # fields = [
        #     # header
        #     Label(text=self.sensor_name),
        #
        #     # read only fields
        #     ReadOnlyField(),
        #     ReadOnlyField(),
        #
        #     # read write fields
        #     ReadWriteField(),
        #     ReadWriteField(),
        #     ReadWriteField(),
        # ]
        #
        # for field in fields:
        #     self.add_widget(field)

        # add header
        main_boxlayout.add_widget(Label(text=self.sensor_name))

        # note that all fields will be displayed in reverse order
        # add input fields
        main_boxlayout.add_widget(ReadWriteField())
        main_boxlayout.add_widget(ReadWriteField())
        main_boxlayout.add_widget(ReadWriteField())
        main_boxlayout.add_widget(ReadWriteField())

        # add read only fields
        main_boxlayout.add_widget(ReadOnlyField())
        main_boxlayout.add_widget(ReadOnlyField())
        main_boxlayout.add_widget(ReadOnlyField())

        # create close button and return result
        close_button = Button(text="Close")

        main_boxlayout.add_widget(close_button)

        return main_boxlayout, close_button


class SchemeLightSensorObserver:
    pass