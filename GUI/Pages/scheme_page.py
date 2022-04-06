from random import random

from kivy.graphics import Canvas, Color, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition, RiseInTransition, \
    NoTransition
from kivy.uix.widget import Widget


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
        self.floors_amount = 0

        # edit tools
        self.edit_button = self._create_edit_button()
        self.edit_tools = EditToolBox(pos_hint={'left':0, 'center_y':.5})

        # create and set up floor selector, screen manager and floor canvases
        self.grid_layout = GridLayout(rows=2, cols=1, size_hint=(1,1))

        self.floor_selector = FloorSelector(self, size_hint=(1,None), size=(1280, 100))
        self.screen_manager = ScreenManager(transition=NoTransition())

        for _ in range(self._get_floors_amount()):
            self.add_floor()

        self.change_floor(self._selected_floor)
        self.floor_selector.select_button(self._selected_floor)

        # add widgets
        self.grid_layout.add_widget(self.screen_manager)
        self.grid_layout.add_widget(self.floor_selector)

        self.add_widget(self.edit_button)
        self.add_widget(self.grid_layout)
        self.add_widget(self.edit_tools)

        # set up edit mode
        if self._edit_mode:
            self.turn_on_edit_mode()
        else:
            self.turn_off_edit_mode()

    def change_floor(self, number:int) -> None:
        self.screen_manager.current = SchemePage._SCREEN_NAME % number
        self._selected_floor = number

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
            pos_hint={'right':1, 'center_y':0.9},
            size=(100,100),
            size_hint=(None, None)
        )
        edit_button.bind(on_press=on_press)
        return edit_button

    def get_selected_floor(self) -> int:
        return self._selected_floor

    def add_floor(self):
        if self.floors_amount >= SchemePage._MAX_FLOORS_AMOUNT:
            return

        screen = Screen(name=SchemePage._SCREEN_NAME % self.floors_amount)
        screen.add_widget(FloorCanvas(self, self.floor_selector))
        self.screen_manager.add_widget(screen)

        self.floor_selector.add_button()

        self.floors_amount += 1

    def save_changes(self):
        # todo
        pass

    def pop_floor(self):
        # todo
        pass

    def _get_floors_amount(self) -> int:
        return 7

    @property
    def MAX_FLOORS_AMOUNT(self) -> int:
        return self._MAX_FLOORS_AMOUNT


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
        if self.schema_page.is_in_edit_mode() and 'line' in touch.ud.keys():
            touch.ud['line'].points += [touch.x, touch.y]

    def _get_floor_data(self) -> dict:
        pass


class FloorSelector(GridLayout):

    _DEFAULT_BUTTON_TEXT = "Floor %d"

    _SELECTED_BUTTON_COLOR = [0,0,0.8,1]
    _UNSELECTED_BUTTON_COLOR = [0.5,0.5,0.5,1]

    def __init__(self, schema_page:SchemePage, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.cols = schema_page.MAX_FLOORS_AMOUNT

        self.schema_page = schema_page
        self.buttons = []

    def add_buttons(self, amount:int) -> None:
        for _ in range(amount):
            self.add_button()

    def select_button(self, index:int) -> None:
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
            self.select_button(button_number)

        button = Button(text=text, size_hint=(1/self.schema_page.MAX_FLOORS_AMOUNT, 1))
        button.bind(on_press=on_press)

        self.buttons.append(button)
        self.add_widget(button)


class EditToolBox(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 6
        self.cols = 1
        self.size = (75, 300)
        self.size_hint = (None, None)

        self.add_widget(Button(text="Add Floor"))
        self.add_widget(Button(text="Pop Floor"))
        self.add_widget(Button(text="Square"))
        self.add_widget(Button(text="Line"))
        self.add_widget(Button(text="Sensor"))
        self.add_widget(Button(text="Save"))