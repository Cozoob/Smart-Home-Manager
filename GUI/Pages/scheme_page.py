from random import random

from kivy.graphics import Canvas, Color, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition, RiseInTransition, \
    NoTransition
from kivy.uix.widget import Widget


class SchemePage(GridLayout):
    _SCREEN_NAME = "Floor %d"
    _EDIT_ON_MESSAGE = "ON"
    _EDIT_OFF_MESSAGE = "OFF"

    def __init__(self, **kwargs):
        # Prepare grid layout
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3

        # own variables
        self._edit_mode = True
        self._selected_floor = 0

        # create and set up floor selector, screen manager and floor canvases
        relative_layout = RelativeLayout()
        self.edit_button = self._create_edit_button()
        self.edit_button.pos = (0,0)

        self.floor_selector = FloorSelector(self)
        self.floor_selector.add_buttons(self._get_floors_amount())
        self.screen_manager = ScreenManager(transition=NoTransition())

        for i in range(self._get_floors_amount()):
            screen = Screen(name=SchemePage._SCREEN_NAME % i)
            screen.add_widget(FloorCanvas(self, i))

            self.screen_manager.add_widget(screen)

        self.change_floor(self._selected_floor)
        self.floor_selector.select_button(self._selected_floor)

        # add widgets
        self.add_widget(self.edit_button)
        # self.add_widget(relative_layout)
        self.add_widget(self.screen_manager)
        self.add_widget(self.floor_selector)

    def change_floor(self, number:int) -> None:
        self.screen_manager.current = SchemePage._SCREEN_NAME % number
        self._selected_floor = number

    def is_in_edit_mode(self):
        return self._edit_mode

    def _create_edit_button(self):
        def on_press(instance):
            self._edit_mode = not self._edit_mode
            instance.text = SchemePage._EDIT_ON_MESSAGE if self._edit_mode else SchemePage._EDIT_OFF_MESSAGE

        edit_button = Button(text=SchemePage._EDIT_ON_MESSAGE if self._edit_mode else SchemePage._EDIT_OFF_MESSAGE)
        edit_button.bind(on_press=on_press)
        return edit_button

    def get_selected_floor(self):
        return self._selected_floor

    def _get_floors_amount(self) -> int:
        return 3


class FloorCanvas(Widget):
    def __init__(self, schema_page:SchemePage, floor_number:int, **kwargs):
        super().__init__(**kwargs)
        self.floor_number = floor_number
        self.schema_page = schema_page

    def on_touch_down(self, touch):
        if self.schema_page.is_in_edit_mode():
            color = (random(), 1, 1)
            with self.canvas:
                Color(*color, mode='hsv')
                touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        if self.schema_page.is_in_edit_mode():
            touch.ud['line'].points += [touch.x, touch.y]

    def _get_floor_data(self) -> dict:
        pass


class FloorSelector(GridLayout):

    _MAX_FLOORS_AMOUNT = 5
    _DEFAULT_BUTTON_TEXT = "Floor %d"

    _SELECTED_BUTTON_COLOR = [0,0,0.8,1]
    _UNSELECTED_BUTTON_COLOR = [0.5,0.5,0.5,1]

    def __init__(self, schema_page:SchemePage, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.cols = FloorSelector._MAX_FLOORS_AMOUNT

        self.schema_page = schema_page
        self.buttons = []

    def add_buttons(self, amount:int):
        for _ in range(amount):
            self.add_button()

    def select_button(self, index:int):
        try:
            for btn in self.buttons:
                btn.background_color = FloorSelector._UNSELECTED_BUTTON_COLOR
            self.buttons[index].background_color = FloorSelector._SELECTED_BUTTON_COLOR
        except IndexError:
            print("Index out of range")

    def add_button(self, **kwargs):

        button_number = len(self.buttons)

        text = kwargs.get('text', None)
        if text is None:
            text = FloorSelector._DEFAULT_BUTTON_TEXT % button_number

        if button_number >= FloorSelector._MAX_FLOORS_AMOUNT:
            return

        def on_press(instance):
            self.schema_page.change_floor(button_number)
            self.select_button(button_number)

        button = Button(text=text)
        button.bind(on_press=on_press)

        self.buttons.append(button)
        self.add_widget(button)
