from typing import Tuple

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout

from GUI.Sensors.PopUpWindowUtils.popup_cycle_field import CycleField
from GUI.Sensors.PopUpWindowUtils.popup_dropdown_field import DropdownField
from GUI.Sensors.PopUpWindowUtils.popup_readonly_field import ReadOnlyField
from GUI.Sensors.PopUpWindowUtils.popup_readwrite_field import ReadWriteField, ReadWriteFieldInt
from GUI.Sensors.scheme_object import SchemeSensor
from Sensors.sensors import Light


class SchemeLightSensor(SchemeSensor):
    # def set_unavailable_state(self): ...
    # def set_available_state(self): ...

    MAIN_IMAGE = "./Resources/SensorIcons/light-bulb-icon.jpg"
    SENSOR_NAME = "SmartLight"

    def __init__(self, sensor:Light, **kwargs):
        super(SchemeLightSensor, self).__init__(self.SENSOR_NAME, sensor, **kwargs)
        self.sensor = sensor
        super().set_background_image(self.MAIN_IMAGE)

    def get_popup_window_content(self) -> Tuple[Layout, Button]:
        main_boxlayout = BoxLayout(orientation="vertical")

        # add header
        main_boxlayout.add_widget(Label(text=self.sensor_name))
        main_boxlayout.add_widget(Label(text="SensorID: " + self.sensor.get_sensor_id()))

        # turn on/off
        turn_on_off = CycleField(["On", "Off"], [self.sensor.turn_on, self.sensor.turn_off])
        turn_on_off.update_value("On" if self.sensor.get_is_turn_on() else "Off")
        main_boxlayout.add_widget(turn_on_off)

        # create close button and return result
        close_button = Button(text="Close")

        main_boxlayout.add_widget(close_button)

        # calculate and set layout size
        children_sizes = [ child.size for child in main_boxlayout.children ]
        main_size = [0,0]
        for child_size in children_sizes:
            main_size[0] = max(main_size[0], child_size[0])
            main_size[1] += child_size[1]

        main_boxlayout.size = main_size
        print(main_boxlayout.size)
        print(children_sizes)

        return main_boxlayout, close_button


class SchemeLightSensorObserver:
    pass
