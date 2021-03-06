from json import JSONDecodeError

from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from typing import List
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown

from os import listdir

import json

from GUI.Pages.settings_page import SettingsPage
from GUI.Sensors.scheme_garage_door import SchemeGarageDoor
from GUI.Sensors.scheme_gas_detector import SchemeGasDetector
from GUI.Sensors.scheme_gas_valve_sensor import SchemeGasValveSensor
from GUI.Sensors.scheme_humid_sensor import SchemeHumidSensor
from GUI.Sensors.scheme_light_sensor import SchemeLightSensor
from GUI.Sensors.scheme_lock_sensor import SchemeLock
from GUI.Sensors.scheme_object import SchemeObject
from GUI.Sensors.scheme_roller_shade import SchemeRollerShade
from GUI.Sensors.scheme_smart_plug import SchemeSmartPlug
from GUI.Sensors.scheme_temperature import SchemeTemperature
from Sensors.enums import SensorType
from Sensors.sensors import (
    Light,
    GasValve,
    SmartPlug,
    Locker,
    GasDetector,
    TemperatureSensor,
    HumidSensor,
    RollerShade,
    GarageDoor,
)


class SchemePage(FloatLayout):
    _SCREEN_NAME = "Floor %d"
    _EDIT_ON_MESSAGE = "EDIT\nON"
    _EDIT_OFF_MESSAGE = "EDIT\nOFF"
    _MAX_FLOORS_AMOUNT = 7

    def __init__(self, **kwargs):
        # Prepare grid layout
        super().__init__(**kwargs)

        # own variables
        self._edit_mode = False
        self._selected_floor = 0
        self.floors = []
        self.screens = []

        # edit tools
        self.edit_button = self._create_edit_button()
        self.edit_tools = EditToolBox(self, pos_hint={"left": 0, "center_y": 0.5})

        # create and set up floor selector, screen manager and floor canvases
        self.grid_layout = GridLayout(rows=2, cols=1, size_hint=(1, 1))

        self.floor_selector = FloorSelector(self, size_hint=(1, None), size=(1280, 100))
        self.screen_manager = ScreenManager(transition=NoTransition())

        # loading data
        self.load_data()

        self.change_floor(self._selected_floor)
        self.floor_selector.select_button(self._selected_floor)

        # add widgets
        self.grid_layout.add_widget(self.screen_manager)
        self.grid_layout.add_widget(self.floor_selector)

        self.add_widget(self.grid_layout)
        self.add_widget(self.edit_button)
        self.add_widget(self.edit_tools)

        # set up edit mode
        if self._edit_mode:
            self.turn_on_edit_mode()
        else:
            self.turn_off_edit_mode()

    def change_floor(self, number: int) -> None:
        self.screen_manager.current = SchemePage._SCREEN_NAME % number
        self._selected_floor = number
        self.floor_selector.select_button(number)

    def is_in_edit_mode(self) -> bool:
        return self._edit_mode

    def turn_on_edit_mode(self):
        if self.edit_tools not in self.children:
            self.add_widget(self.edit_tools)

    def turn_off_edit_mode(self):
        if self.edit_tools in self.children:
            self.remove_widget(self.edit_tools)

    def _create_edit_button(self) -> Button:
        def on_press(instance):
            self._edit_mode = not self._edit_mode
            instance.text = (
                SchemePage._EDIT_ON_MESSAGE
                if self._edit_mode
                else SchemePage._EDIT_OFF_MESSAGE
            )
            if self._edit_mode:
                self.turn_on_edit_mode()
            else:
                self.turn_off_edit_mode()

        edit_button = Button(
            text=SchemePage._EDIT_ON_MESSAGE
            if self._edit_mode
            else SchemePage._EDIT_OFF_MESSAGE,
            pos_hint={"right": 1, "center_y": 0.9},
            size=(100, 100),
            size_hint=(None, None),
        )
        edit_button.bind(on_press=on_press)
        return edit_button

    def get_current_floor_index(self) -> int:
        return self._selected_floor

    def add_floor(self):
        if len(self.floors) >= SchemePage._MAX_FLOORS_AMOUNT:
            return

        self.add_floor_press_ok()

    def pop_up_window_add_floor(self):
        self.__popup_window_scheme(
            label_text="Provide the name of file with extension for the picture!",
            button_text="Add",
            title="Add floor",
            fun_on_press=self.add_floor_press_ok,
        )

    def add_floor_press_ok(self, filename: str = ""):

        screen = Screen(name=SchemePage._SCREEN_NAME % len(self.floors))
        floor = FloorCanvas(self, len(self.floors), filename)
        screen.add_widget(floor)
        self.screen_manager.add_widget(screen)
        self.floors.append(floor)
        self.screens.append(screen)

        self.floor_selector.add_button()

    def save_changes(self):
        print("Save scheme changes...")

        data = []

        for idx, floor in enumerate(self.floors):
            data.append({"floor": {"image": ""}, "sensors": []})

            data_floor = floor.save_floor_data()
            image_name = data_floor[0]
            sensors_data = data_floor[1:]

            data[idx]["floor"]["image"] = image_name

            for sensor in sensors_data:
                data[idx]["sensors"].append(sensor)

        try:
            with open("./Data/scheme.json", "w") as file:
                json.dump(data, file)
        except FileNotFoundError:
            print("Cannot save changes.")

    def load_data(self):
        print("Loading scheme data in scheme page.")
        with open("./Data/scheme.json", "r") as scheme_file:
            try:
                data = json.loads(scheme_file.read())
            except JSONDecodeError:
                data = []

            if len(data) == 0:
                for _ in range(1):
                    self.add_floor()

                # save this...
                self.save_changes()
                return

            for i, floor_data in enumerate(data):
                filename = floor_data["floor"]["image"]
                self.add_floor_press_ok(filename)

                curr_floor = self.floors[i]
                sensors = floor_data["sensors"]

                for sensor in sensors:
                    curr_floor.add_sensor(
                        SensorType[sensor.get("type")],
                        sensor.get("topic"),
                        size=[sensor.get("width"), sensor.get("width")],
                        pos=[sensor.get("x"), sensor.get("y")],
                    )

    def pop_floor(self):
        if len(self.floors) <= 1:
            return

        if self._selected_floor == len(self.floors) - 1:
            self.change_floor(len(self.floors) - 2)
        self.floors.pop()
        screen = self.screens.pop()
        self.screen_manager.remove_widget(screen)
        self.floor_selector.pop_button()

    def _get_schema_floors_amount(self) -> int:
        return len(self.floors)

    def get_current_floor(self):
        return self.floors[self._selected_floor]

    def edit_scheme(self):
        self.__popup_window_scheme(
            label_text="Provide the name of file with extension for the picture!",
            button_text="Edit",
            title="Edit scheme",
            fun_on_press=self.floors[self._selected_floor].edit_scheme,
        )

    def __popup_window_scheme(
        self, label_text: str, button_text: str, title: str, fun_on_press
    ):
        """
        :param fun_on_press: Must be a function with :param filename: str.
        """
        boxlayout = BoxLayout(orientation="vertical")
        boxlayout.add_widget(
            Label(text=label_text, size=(370, 35), size_hint=[None, None])
        )
        inp_area = TextInput(text="", size=(370, 35), size_hint=[None, None])
        boxlayout.add_widget(inp_area)

        save_close_button = Button(
            text=button_text, size=(50, 50), size_hint=[None, None]
        )
        boxlayout.add_widget(save_close_button)

        popup = Popup(
            title=title, content=boxlayout, size_hint=(None, None), size=(400, 200)
        )

        def __close_add_floor(instance):
            popup.dismiss()
            filename = inp_area.text

            fun_on_press(filename)

        save_close_button.bind(on_press=__close_add_floor)
        popup.open()

    @property
    def MAX_FLOORS_AMOUNT(self) -> int:
        return self._MAX_FLOORS_AMOUNT


class FloorCanvas(RelativeLayout):
    counter = NumericProperty(0)
    image_names = [img for img in listdir("./Resources/Images/")]

    def __init__(
        self, schema_page: SchemePage, floor_number: int, filename: str, **kwargs
    ):
        super().__init__(**kwargs)

        self.floor_number = floor_number
        self.schema_page = schema_page
        self.objects: List[SchemeObject] = []
        self.selected_object: SchemeObject = None

        with self.canvas:
            Color(1, 1, 1)
            self.rect = Rectangle(pos=self.center, size=(self.width, self.height))

            self.bind(pos=self._update_rect, size=self._update_rect)

        if filename not in self.image_names:
            filename = "noimage.jpg"

        self.image_name = filename
        self.image = self.load_image(self.image_name)
        self.add_widget(self.image)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        self.selected_object = None
        for obj in self.objects:
            obj.unselect()

        # find and select one that collides
        for obj in self.objects[::-1]:
            if obj.collide_point(*touch.pos):
                self.selected_object = obj
                obj.select()

                break

        if not self.schema_page.is_in_edit_mode():
            if self.selected_object:
                self.selected_object.show_popup_window()

    def on_touch_move(self, touch):
        if self.schema_page.is_in_edit_mode():

            if self.selected_object is not None:
                self.selected_object.center = touch.pos

    def on_touch_up(self, touch):
        if self.schema_page.is_in_edit_mode():
            pass

    def _get_floor_data(self) -> list:
        pass

    def save_floor_data(self) -> list:
        # the first position is always image filename
        arr = [self.image_name]

        for obj in self.objects:
            arr.append(obj.get_data())

        return arr

    def add_sensor(self, sensor_type: SensorType, sensor_topic: str, **kwargs):

        try:
            with open("./Data/user.json", "r") as file:
                data = json.loads(file.read())
                SettingsPage.broker_ip = data["Broker_IP"]
                SettingsPage.broker_port = int(data["Broker_Port"])

        except FileNotFoundError:
            return

        if "pos" not in kwargs:
            kwargs["pos"] = [30, 30]

        if sensor_type == SensorType.LIGHT:
            sensor = Light(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeLightSensor(sensor, **kwargs)
        elif sensor_type == SensorType.GAS_VALVE:
            sensor = GasValve(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeGasValveSensor(sensor, **kwargs)
        elif sensor_type == SensorType.SMART_PLUG:
            sensor = SmartPlug(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeSmartPlug(sensor, **kwargs)
        elif sensor_type == SensorType.LOCKER:
            sensor = Locker(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeLock(sensor, **kwargs)
        elif sensor_type == SensorType.GAS_DETECTOR:
            sensor = GasDetector(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeGasDetector(sensor, **kwargs)
        elif sensor_type == SensorType.TEMPERATURE:
            sensor = TemperatureSensor(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeTemperature(sensor, **kwargs)
        elif sensor_type == SensorType.HUMID:
            sensor = HumidSensor(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeHumidSensor(sensor, **kwargs)
        elif sensor_type == SensorType.ROLLER_SHADE:
            sensor = RollerShade(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeRollerShade(sensor, **kwargs)
        elif sensor_type == SensorType.GARAGE_DOOR:
            sensor = GarageDoor(
                sensor_topic, SettingsPage.broker_ip, SettingsPage.broker_port
            )
            scheme_sensor = SchemeGarageDoor(sensor, **kwargs)
        else:
            return

        self.add_widget(scheme_sensor)
        self.objects.append(scheme_sensor)

    def remove_selected_object(self):
        if self.selected_object is None:
            return

        self.selected_object.sensor.disconnect()
        self.selected_object.unselect()
        self.remove_widget(self.selected_object)
        self.objects.remove(self.selected_object)
        self.selected_object = None

    def edit_scheme(self, filename: str):
        self.remove_widget(self.image)
        if filename not in self.image_names:
            filename = "noimage.jpg"

        self.image_name = filename
        self.image = self.load_image(self.image_name)
        self.add_widget(self.image, index=10)
        # with self.canvas.before:
        # Color(0,0,0)
        # Rectangle(source=image_name)
        # self.bind(...)

    def pop_up_window_add_sensor(self):
        boxlayout = BoxLayout(orientation="vertical")
        boxlayout.add_widget(Label(text="Provide data"))
        inp_area = TextInput(text="", multiline=False)
        boxlayout.add_widget(inp_area)

        selected_sensor_type = None

        def show_dropdown(button, *args):
            def fun_factory(sensor_type):
                return lambda dropdown_button: on_select(dropdown_button, sensor_type)

            def on_select(dropdown_button, sensor_type: SensorType):
                nonlocal selected_sensor_type, dp
                dp.select(dropdown_button.text)
                selected_sensor_type = sensor_type

            dp = DropDown()
            dp.bind(on_select=lambda instance, x: setattr(button, "text", x))
            for sensor_type in SensorType:
                item = Button(text=sensor_type.name, size_hint_y=None, height=44)
                item.bind(on_release=fun_factory(sensor_type))
                dp.add_widget(item)
            dp.open(button)

        type_select_button = Button(text="Chose Type")
        type_select_button.bind(on_release=show_dropdown)

        boxlayout.add_widget(type_select_button)

        save_close_button = Button(text="Add sensor")
        boxlayout.add_widget(save_close_button)

        popup = Popup(
            title="Add sensor",
            content=boxlayout,
            size_hint=(None, None),
            size=(400, 250),
        )

        def __close_add_floor(instance):
            sensor_topic = inp_area.text
            if sensor_topic == "" or selected_sensor_type is None:
                return

            self.add_sensor(selected_sensor_type, sensor_topic)
            popup.dismiss()
            # todo

        save_close_button.bind(on_press=__close_add_floor)
        popup.open()

    def load_image(self, image_name: str) -> Image:
        try:
            file_path = "./Resources/Images/" + image_name
            with open(file_path, "r"):
                return Image(source=file_path)
        except FileNotFoundError:
            pass


class FloorSelector(GridLayout):
    _DEFAULT_BUTTON_TEXT = "Floor %d"

    _SELECTED_BUTTON_COLOR = [0, 0, 0.8, 1]
    _UNSELECTED_BUTTON_COLOR = [0.5, 0.5, 0.5, 1]

    def __init__(self, schema_page: SchemePage, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.cols = schema_page.MAX_FLOORS_AMOUNT

        self.schema_page = schema_page
        self.buttons = []

    def add_buttons(self, amount: int) -> None:
        for _ in range(amount):
            self.add_button()

    def select_button(self, index: int) -> None:
        try:
            for btn in self.buttons:
                btn.background_color = FloorSelector._UNSELECTED_BUTTON_COLOR
            self.buttons[index].background_color = FloorSelector._SELECTED_BUTTON_COLOR
        except IndexError:
            print("Index out of range")

    def add_button(self, **kwargs) -> None:

        button_number = len(self.buttons)

        text = kwargs.get("text", None)
        if text is None:
            text = FloorSelector._DEFAULT_BUTTON_TEXT % button_number

        if button_number >= self.schema_page.MAX_FLOORS_AMOUNT:
            return

        def on_press(instance):
            self.schema_page.change_floor(button_number)

        button = Button(
            text=text, size_hint=(1 / self.schema_page.MAX_FLOORS_AMOUNT, 1)
        )
        button.bind(on_press=on_press)
        button.background_color = FloorSelector._UNSELECTED_BUTTON_COLOR

        self.buttons.append(button)
        self.add_widget(button)

    def pop_button(self):
        if len(self.buttons) <= 1:
            return

        button = self.buttons.pop()
        self.remove_widget(button)


class EditToolBox(GridLayout):
    def __init__(self, schema_page: SchemePage, **kwargs):
        super().__init__(**kwargs)
        self.rows = 6
        self.cols = 1
        self.size = (75, 350)
        self.size_hint = (None, None)

        # own variables
        self.schema_page = schema_page

        # button functions
        def add(instance):
            self.schema_page.add_floor()

        def pop(instance):
            self.schema_page.pop_floor()

        def sensor_add(instance):
            self.schema_page.get_current_floor().pop_up_window_add_sensor()

        def sensor_remove(instance):
            self.schema_page.get_current_floor().remove_selected_object()

        def scheme(instance):
            self.schema_page.edit_scheme()

        def save(instance):
            self.schema_page.save_changes()

        # defining buttons
        texts = ["Add Floor", "Pop Floor", "+ Sensor", "- Sensor", "Edit photo", "Save"]
        functions = [add, pop, sensor_add, sensor_remove, scheme, save]

        for text, f in zip(texts, functions):
            button = Button(text=text)
            button.bind(on_press=f)
            self.add_widget(button)
