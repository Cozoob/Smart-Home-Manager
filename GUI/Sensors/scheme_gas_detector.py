from typing import Tuple

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout

from GUI.Sensors.PopUpWindowUtils.popup_readonly_field import ReadOnlyField
from GUI.Sensors.scheme_object import SchemeSensor
from Sensors.sensors import GasDetector


class SchemeGasDetector(SchemeSensor):

    MAIN_IMAGE = "./Resources/SensorIcons/gas-detector-icon.jpg"
    SENSOR_NAME = "GasDetector"
    REFRESH_RATE_SECONDS = 1

    def __init__(self, sensor: GasDetector, **kwargs):
        super(SchemeGasDetector, self).__init__(self.SENSOR_NAME, sensor, **kwargs)
        self.sensor = sensor

        super().set_background_image(self.MAIN_IMAGE)

    def get_popup_window_content(self) -> Tuple[Layout, Button]:
        main_boxlayout = BoxLayout(orientation="vertical")

        def update(*args):
            nonlocal gas_density, gas_detected
            gas_density.update_value(self.sensor.check_gas_density())
            gas_detected.update_value(self.sensor.get_is_gas_detected())
            pass

        # add header
        main_boxlayout.add_widget(Label(text=self.sensor_name))
        main_boxlayout.add_widget(
            Label(text="SensorID: " + self.sensor.get_sensor_id())
        )

        # todo
        gas_density = ReadOnlyField("Gas Density: ")
        main_boxlayout.add_widget(gas_density)

        gas_detected = ReadOnlyField("Gas Detected: ")
        main_boxlayout.add_widget(gas_detected)

        # clock update
        clock = Clock.schedule_interval(update, self.REFRESH_RATE_SECONDS)

        # create close button and return result
        close_button = Button(text="Close")
        close_button.bind(on_press=lambda _: clock.cancel())

        main_boxlayout.add_widget(close_button)

        # calculate and set layout size
        children_sizes = [child.size for child in main_boxlayout.children]
        main_size = [0, 0]
        for child_size in children_sizes:
            main_size[0] = max(main_size[0], child_size[0])
            main_size[1] += child_size[1]

        main_boxlayout.size = main_size

        return main_boxlayout, close_button
