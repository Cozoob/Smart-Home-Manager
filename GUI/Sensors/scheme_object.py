from abc import abstractmethod
from typing import Tuple

from kivy.graphics import Ellipse, Line, Color
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from Sensors.sensors import Sensor


class SchemeObject(FloatLayout):
    """
    Abstract class
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.size_hint = [None, None]

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def unselect(self):
        pass

    # @abstractmethod
    # def set_unavailable_state(self):
    #     pass
    #
    # @abstractmethod
    # def set_available_state(self):
    #     pass

    @abstractmethod
    def show_popup_window(self):
        pass


class SchemeSensor(SchemeObject):

    def __init__(self, sensor_name: str, sensor:Sensor, **kwargs):
        super().__init__(**kwargs)
        self.size = [50, 50]
        self.selected = False
        self.sensor_name = sensor_name
        self.sensor = sensor

        self.sensor_icon: Widget = None
        self.label: Label = None

        self._add_name_label()

        with self.canvas.before:

            Color(0.2, 0.2, 0.2)

            self.background_ellipse = Ellipse(pos=self.pos, size=self.size)

            self.line = Line(
                rectangle=(self.x, self.y, 0, 0), width=1, dash_length=5, dash_offset=2
            )

        self.bind(pos=self._update_ellipse, size=self._update_ellipse)
        self.bind(pos=self._update_line, size=self._update_line)

        self.unselect()

    def _update_ellipse(self, *args):
        self.background_ellipse.pos = self.pos
        self.background_ellipse.size = self.size

    def _update_line(self, *args):
        if self.selected:
            self.line.rectangle = (
                self.x - 5,
                self.y - 5,
                self.width + 10,
                self.height + 10,
            )
        else:
            self.line.rectangle = (self.x, self.y, 0, 0)

    def _update_icon(self, *args):
        if self.sensor_icon:
            self.sensor_icon.center = self.center

    def set_background_image(self, image_path: str):
        if self.sensor_icon:
            self.remove_widget(self.sensor_icon)

        self.sensor_icon = SensorIcon(
            image_path,
            size_hint=[0.85, 0.85],
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.sensor_icon)
        self.bind(pos=self._update_icon, size=self._update_icon)

    def _add_name_label(self):
        self._remove_name_label()

        self.label = Label(
            text=f"[color=000000]{self.sensor_name}[/color]",
            pos_hint={"center_x": 0.5, "center_y": -0.1},
            markup=True,
        )

        self.add_widget(self.label)

    def _remove_name_label(self):
        if self.label:
            self.remove_widget(self.label)

    def get_data(self):
        return {
            "x": self.pos[0],
            "y": self.pos[1],
            "width": self.size[0],
            "height": self.size[1],
            "type": self.sensor.get_sensor_type().name,
            "topic": self.sensor.get_sensor_id(),
        }

    def select(self):
        self.selected = True
        self._update_line()
        self._update_ellipse()

    def unselect(self):
        self.selected = False
        self._update_line()
        self._update_ellipse()

    def show_popup_window(self):
        content, button = self.get_popup_window_content()

        popup = Popup(
            title="Sensor Details",
            content=content,
            size_hint=(None, None),
            size=content.size,
            auto_dismiss=False
        )

        button.bind(on_press=popup.dismiss)
        button.bind(on_press=popup.dismiss)
        popup.open()

    @abstractmethod
    def get_popup_window_content(self) -> Tuple[Layout, Button]:
        pass


class SensorIcon(Widget):
    def __init__(self, image_path: str, **kwargs):
        super().__init__(**kwargs)

        self.image_path = image_path
        with self.canvas:
            Color(1, 1, 1, 1)
            self.image_ellipse = Ellipse(pos=self.pos, size=self.size)
            self.image_ellipse.source = self.image_path

        self.bind(pos=self._update_ellipse, size=self._update_ellipse)

    def _update_ellipse(self, *args):
        self.image_ellipse.pos = self.pos
        self.image_ellipse.size = self.size
