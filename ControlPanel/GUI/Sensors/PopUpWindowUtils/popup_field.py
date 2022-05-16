from abc import abstractmethod

from kivy.uix.boxlayout import BoxLayout


class Field(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (400, 30)
        self.size_hint = (None, None)

    @abstractmethod
    def update_value(self, value) -> bool:
        ...
