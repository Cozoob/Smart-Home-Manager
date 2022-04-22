from random import random

from abc import abstractproperty, abstractmethod, ABC

from kivy.graphics import Canvas, Color, Ellipse, Line
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition, RiseInTransition, \
    NoTransition
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from typing import List
from kivy.uix.image import Image

from os import listdir

import json

# def get_max_floors_amount():
#     return SchemePage._MAX_FLOORS_AMOUNT
Builder.load_file("GUI/Pages/scheme_page.kv")


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
        self.edit_tools = EditToolBox(self, pos_hint={'left': 0, 'center_y': .5})

        # create and set up floor selector, screen manager and floor canvases
        self.grid_layout = GridLayout(rows=2, cols=1, size_hint=(1, 1))

        self.floor_selector = FloorSelector(self, size_hint=(1, None), size=(1280, 100))
        self.screen_manager = ScreenManager(transition=NoTransition())

        for _ in range(self._get_schema_floors_amount()):
            self.add_floor_press_ok("")

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
            instance.text = SchemePage._EDIT_ON_MESSAGE if self._edit_mode else SchemePage._EDIT_OFF_MESSAGE
            if self._edit_mode:
                self.turn_on_edit_mode()
            else:
                self.turn_off_edit_mode()

        edit_button = Button(
            text=SchemePage._EDIT_ON_MESSAGE if self._edit_mode else SchemePage._EDIT_OFF_MESSAGE,
            pos_hint={'right': 1, 'center_y': 0.9},
            size=(100, 100),
            size_hint=(None, None)
        )
        edit_button.bind(on_press=on_press)
        return edit_button

    def get_current_floor_index(self) -> int:
        return self._selected_floor

    def add_floor(self):
        if len(self.floors) >= SchemePage._MAX_FLOORS_AMOUNT:
            return

        self.__popup_window_scheme(label_text='Provide the name of file with extension for the picture!',
                                   button_text='Add', title='Add floor', fun_on_press=self.add_floor_press_ok)

    def add_floor_press_ok(self, filename: str):

        screen = Screen(name=SchemePage._SCREEN_NAME % len(self.floors))
        floor = FloorCanvas(self, len(self.floors), filename)
        screen.add_widget(floor)
        self.screen_manager.add_widget(screen)
        self.floors.append(floor)
        self.screens.append(screen)

        self.floor_selector.add_button()

    def save_changes(self):
        # todo
        values = []
        for floor in self.floors:
            values.append(floor.saved_floor_data())

        try:
            with open("./Data/tmp.json", "w") as file:
                json.dump(values, file)
        except FileNotFoundError:
            print("Cannot save changes.")

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
        return 2

    def get_current_floor(self):
        return self.floors[self._selected_floor]

    def edit_scheme(self):
        self.__popup_window_scheme(label_text='Provide the name of file with extension for the picture!',
                                   button_text='Edit', title='Edit scheme',
                                   fun_on_press=self.floors[self._selected_floor].edit_scheme)

    def __popup_window_scheme(self, label_text: str, button_text: str, title: str, fun_on_press):
        """
        :param fun_on_press: Must be a function with :param filename: str.
        """
        boxlayout = BoxLayout(orientation="vertical")
        boxlayout.add_widget(Label(text=label_text, size=(370, 35),
                                   size_hint=[None, None]))
        inp_area = TextInput(text='', size=(370, 35), size_hint=[None, None])
        boxlayout.add_widget(inp_area)

        save_close_button = Button(text=button_text, size=(50, 50), size_hint=[None, None])
        boxlayout.add_widget(save_close_button)

        popup = Popup(title=title,
                      content=boxlayout,
                      size_hint=(None, None), size=(400, 200))

        def __close_add_floor(instance):
            popup.dismiss()
            filename = inp_area.text

            fun_on_press(filename)

        save_close_button.bind(on_press=__close_add_floor)
        popup.open()

    @property
    def MAX_FLOORS_AMOUNT(self) -> int:
        return self._MAX_FLOORS_AMOUNT


class SchemeObject(BoxLayout):
    """
    Abstract class
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.size_hint = [None, None]

    # def on_touch_down(self, touch):
    #     self.selected = True
    #
    # def on_touch_up(self, touch):
    #     self.selected = False

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def change_position(self, pos):
        pass

    @abstractmethod
    def change_size(self, size):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def unselect(self):
        pass


class SchemeSensor(SchemeObject):
    counter = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Drag me!", pos=self.pos)

    def get_data(self):
        return {
            "x": self.pos[0],
            "y": self.pos[1],
            "width": self.size[0],
            "height": self.size[1],
            "type": self.sensor.type,
            "topic": self.sensor.topic
        }

    def change_position(self, pos):
        self.pos = pos

    def change_size(self, size):
        pass
        # self.size = size

    def select(self):
        pass

    def unselect(self):
        pass


class FloorCanvas(RelativeLayout):
    counter = NumericProperty(0)
    # selected = ObjectProperty(None)
    sel = BooleanProperty(False)
    image_names = [img for img in listdir("./Resources/Images/")]

    def __init__(self, schema_page: SchemePage, floor_number: int, filename: str, **kwargs):
        super().__init__(**kwargs)

        self.floor_number = floor_number
        self.schema_page = schema_page
        self.objects: List[SchemeObject] = []

        if filename not in self.image_names:
            filename = "noimage.jpg"

        image_name = filename
        self.image = self.load_image(image_name)
        self.add_widget(self.image)

    def on_touch_down(self, touch):
        if touch.x < 100 and touch.y < 100:
            return super(FloorCanvas, self).on_touch_down(touch)
        if self.select.state == 'down':
            for child in self.children:
                if child.collide_point(*touch.pos):
                    self.selected = child
                    self.sel = True
                    with self.canvas:
                        Color(0, 0, 0)
                        touch.ud['line'] = Line(rectangle=(child.x - 5,
                                                           child.y - 5, child.width + 10, child.height + 10),
                                                dash_length=5, dash_offset=2)
                    break

    def on_touch_move(self, touch):
        if self.select.state == 'down' and self.sel == True:
            self.canvas.remove(touch.ud['line'])
            child = self.selected
            child.center = touch.pos
            with self.canvas:
                touch.ud['line'] = Line(rectangle=(child.x - 5, child.y - 5,
                                                   child.width + 10, child.height + 10), width=1,
                                        dash_length=5, dash_offset=2)

    def on_touch_up(self, touch):
        if self.select.state == 'down' and self.sel == True:
            self.canvas.remove(touch.ud['line'])
            self.sel = False
        if touch.x < 100 and touch.y < 100:
            return super(FloorCanvas, self).on_touch_down(touch)
        if self.draw.state == 'down':
            self.counter += 1
            ball = SchemeSensor()
            ball.center = touch.pos
            ball.counter = self.counter
            self.objects.append(ball)
            self.add_widget(ball)

    def _get_floor_data(self) -> list:
        pass

    def saved_floor_data(self) -> list:
        arr = []
        for obj in self.objects:
            arr.append(obj.get_data())
        return arr

    def add_rectangle(self):
        pass

    def add_sensor(self):
        pass

    def edit_scheme(self, filename: str):
        self.remove_widget(self.image)
        if filename not in self.image_names:
            filename = "noimage.jpg"

        print(filename)
        image_name = filename
        self.image = self.load_image(image_name)
        self.add_widget(self.image)

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

        text = kwargs.get('text', None)
        if text is None:
            text = FloorSelector._DEFAULT_BUTTON_TEXT % button_number

        if button_number >= self.schema_page.MAX_FLOORS_AMOUNT:
            return

        def on_press(instance):
            self.schema_page.change_floor(button_number)

        button = Button(text=text, size_hint=(1 / self.schema_page.MAX_FLOORS_AMOUNT, 1))
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
        self.rows = 5
        self.cols = 1
        self.size = (75, 300)
        self.size_hint = (None, None)

        # own variables
        self.schema_page = schema_page

        # button functions
        def add(instance):
            self.schema_page.add_floor()

        def pop(instance):
            self.schema_page.pop_floor()

        def sensor(instance):
            self.schema_page.get_current_floor()

        def scheme(instance):
            self.schema_page.edit_scheme()

        def save(instance):
            self.schema_page.save_changes()

        # defining buttons
        texts = ["Add Floor", "Pop Floor", "Sensor", "Edit photo", "Save"]
        functions = [add, pop, sensor, scheme, save]

        for text, f in zip(texts, functions):
            button = Button(text=text)
            button.bind(on_press=f)
            self.add_widget(button)

        # adding drawing option
