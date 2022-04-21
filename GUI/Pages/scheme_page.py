from random import random

from abc import abstractproperty, abstractmethod

from kivy.graphics import Canvas, Color, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition, RiseInTransition, \
    NoTransition
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color


def get_max_floors_amount():
    return SchemePage._MAX_FLOORS_AMOUNT


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
            self.add_floor()

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

        screen = Screen(name=SchemePage._SCREEN_NAME % len(self.floors))
        floor = FloorCanvas(self, self.floor_selector)
        screen.add_widget(floor)
        self.screen_manager.add_widget(screen)
        self.floors.append(floor)
        self.screens.append(screen)

        self.floor_selector.add_button()

    def save_changes(self):
        # todo
        pass

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

    @property
    def MAX_FLOORS_AMOUNT(self) -> int:
        return self._MAX_FLOORS_AMOUNT


class SchemeObject(Widget):
    """
    Abstract class
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


class SchemeRectangle(SchemeObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_data(self):
        return {
            "x": self.pos.x,
            "y": self.pos.y,
            "width": self.size.x,
            "height": self.size.y,
        }

    def change_position(self, pos):
        self.pos = pos

    def change_size(self, size):
        pass
        # self.size = size

    def select(self):
        pass


class SchemeSensor(SchemeObject):

    def __init__(self, sensor, **kwargs):
        super().__init__(**kwargs)
        self.sensor = sensor

    def get_data(self):
        return {
            "x": self.pos.x,
            "y": self.pos.y,
            "width": self.size.x,
            "height": self.size.y,
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


class FloorCanvas(Widget):
    def __init__(self, schema_page: SchemePage, floor_number: int, **kwargs):
        super().__init__(**kwargs)
        self.floor_number = floor_number
        self.schema_page = schema_page
        self.objects: list[SchemeObject] = []

        # Arranging Canvas
        with self.canvas:
            Color(0,0,0,.5)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width,
                                        self.height))

            # Update the canvas as the screen size change
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

        # update function which makes the canvas adjustable.

        self.add_rectangle()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _get_floor_data(self) -> list:
        pass

    def save_floor_data(self) -> list:
        pass

    def add_rectangle(self):
        self.canvas.add(Rectangle())

    def add_sensor(self):
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
        self.rows = 6
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

        def square(instance):
            self.schema_page.get_current_floor()

        def line(instance):
            self.schema_page.get_current_floor()

        def sensor(instance):
            self.schema_page.get_current_floor()

        def save(instance):
            self.schema_page.save_changes()

        # defining buttons
        texts = ["Add Floor", "Pop Floor", "Square", "Line", "Sensor", "Save"]
        functions = [add, pop, square, line, sensor, save]

        for text, f in zip(texts, functions):
            button = Button(text=text)
            button.bind(on_press=f)
            self.add_widget(button)
