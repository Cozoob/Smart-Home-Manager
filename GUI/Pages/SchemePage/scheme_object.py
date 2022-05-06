from abc import abstractmethod

from kivy.graphics import Ellipse, Line
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class SchemeObject(BoxLayout):
    """
    Abstract class
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.size_hint = [None, None]


    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def change_position(self, pos):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def unselect(self):
        pass

    @abstractmethod
    def set_unavailable_state(self):
        pass

    @abstractmethod
    def set_available_state(self):
        pass

    @abstractmethod
    def show_popup_window(self):
        pass


class SchemeSensor(SchemeObject):

    __DEFAULT_COLOR = [.2, .2, .2]
    __UNAVAILABLE_COLOR = [.5, .0, .0]

    counter = NumericProperty(0)
    color = ListProperty(__DEFAULT_COLOR)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = [50, 50]
        self.selected = False
        self.set_available_state()
        with self.canvas:

            self.ellipse = Ellipse(pos=self.pos, size=self.size)

            self.line = Line(rectangle=(self.x, self.y, 0, 0), width=1,
                             dash_length=5, dash_offset=2)

        self.bind(pos=self._update_ellipse, size=self._update_ellipse)
        self.bind(pos=self._update_line, size=self._update_line)

    def _update_ellipse(self, *args):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size

    def _update_line(self, *args):
        if self.selected:
            self.line.rectangle = (self.x - 5, self.y - 5,
                                   self.width + 10, self.height + 10)
        else:
            self.line.rectangle = (self.x,self.y,0,0)

    def get_data(self):
        return {
            "x": self.pos[0],
            "y": self.pos[1],
            "width": self.size[0],
            "height": self.size[1],
            "type": self.sensor.type,
            "topic": self.sensor.sender_topic
        }

    def change_position(self, pos):
        self.pos = pos

    def select(self):
        self.selected = True
        self._update_line()
        self._update_ellipse()

    def unselect(self):
        self.selected = False
        self._update_line()
        self._update_ellipse()

    def set_unavailable_state(self):
        self.color = self.__UNAVAILABLE_COLOR

    def set_available_state(self):
        self.color = self.__DEFAULT_COLOR

    def show_popup_window(self):
        boxlayout = BoxLayout(orientation="vertical")
        boxlayout.add_widget(Label(text="Sensor details", size=(370, 35),
                                   size_hint=[None, None]))
        inp_area = TextInput(text='', size=(370, 35), size_hint=[None, None])
        boxlayout.add_widget(inp_area)

        save_close_button = Button(text="Close", size=(50, 50), size_hint=[None, None])
        boxlayout.add_widget(save_close_button)

        popup = Popup(title='Add sensor',
                      content=boxlayout,
                      size_hint=(None, None), size=(400, 200))

        save_close_button.bind(on_press=popup.dismiss)
        popup.open()
