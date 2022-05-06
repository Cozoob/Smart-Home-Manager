from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from GUI.Sensors.PopUpWindowUtils.popup_field import Field


class ReadOnlyField(Field):
    def update_value(self):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.add_widget(Label(text="Filed name:"))
        self.add_widget(TextInput())
        self.add_widget(Button(text="OK"))
