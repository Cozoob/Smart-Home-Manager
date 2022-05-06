from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from GUI.Sensors.PopUpWindowUtils.popup_field import Field


class ReadWriteField(Field):

    def update_value(self):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'horizontal'
        self.add_widget(Label(text="Filed name:"))
        self.add_widget(Label(text="Field read only value"))


class ReadWriteFieldInt(ReadWriteField): ...
class ReadWriteFieldFloat(ReadWriteField): ...