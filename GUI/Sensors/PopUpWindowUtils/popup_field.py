from abc import abstractmethod

from kivy.uix.boxlayout import BoxLayout


class Field(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def update_value(self):
        ...
