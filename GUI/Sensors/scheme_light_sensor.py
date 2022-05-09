from typing import Tuple

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout

from GUI.Sensors.PopUpWindowUtils.popup_cycle_field import CycleField
from GUI.Sensors.PopUpWindowUtils.popup_dropdown_field import DropdownField
from GUI.Sensors.PopUpWindowUtils.popup_readonly_field import ReadOnlyField
from GUI.Sensors.PopUpWindowUtils.popup_readwrite_field import ReadWriteField, ReadWriteFieldInt
from GUI.Sensors.scheme_object import SchemeSensor
from Sensors.enums import ColorTemperature
from Sensors.sensors import Light


class SchemeLightSensor(SchemeSensor):

    MAIN_IMAGE = "./Resources/SensorIcons/light-bulb-icon.jpg"
    SENSOR_NAME = "SmartLight"
    REFRESH_RATE_SECONDS = 1

    def __init__(self, sensor:Light, **kwargs):
        super(SchemeLightSensor, self).__init__(self.SENSOR_NAME, sensor, **kwargs)
        self.sensor = sensor
        super().set_background_image(self.MAIN_IMAGE)

    def get_popup_window_content(self) -> Tuple[Layout, Button]:
        main_boxlayout = BoxLayout(orientation="vertical")

        def update(*args):
            nonlocal turn_state, brightness_state
            turn_state.update_value("ON" if self.sensor.get_is_turn_on() else "OFF")
            brightness_state.update_value(self.sensor.get_brightness())
            color_state.update_value(self.sensor.get_color_temperature().name)

        # add header
        main_boxlayout.add_widget(Label(text=self.sensor_name))
        main_boxlayout.add_widget(Label(text="SensorID: " + self.sensor.get_sensor_id()))

        # turn on/off
        turn_state = ReadOnlyField("State:")
        main_boxlayout.add_widget(turn_state)

        turn_on_off = CycleField(["On", "Off"], [self.sensor.turn_on, self.sensor.turn_off])
        turn_on_off.update_value("On" if self.sensor.get_is_turn_on() else "Off")
        main_boxlayout.add_widget(turn_on_off)

        # brightness
        brightness_state = ReadOnlyField("Brightness:")
        main_boxlayout.add_widget(brightness_state)

        brightness = ReadWriteFieldInt("Brightness(0-100):", self.sensor.set_brightness, 0, 100)
        brightness.update_value(self.sensor.get_brightness())
        main_boxlayout.add_widget(brightness)

        # color temperature
        color_state = ReadOnlyField("Color temperature:")
        main_boxlayout.add_widget(color_state)

        def fun_factory(clr:ColorTemperature):
            return lambda : self.sensor.set_color_temperature(clr)

        color = DropdownField(
            [clr.name for clr in ColorTemperature],
            [fun_factory(clr) for clr in ColorTemperature]
        )

        color.update_value(self.sensor.get_color_temperature().name)
        main_boxlayout.add_widget(color)

        # clock update
        clock = Clock.schedule_interval(update, self.REFRESH_RATE_SECONDS)

        # create close button and return result
        close_button = Button(text="Close")
        close_button.bind(on_press=lambda _: clock.cancel())

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

