from typing import List

from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from GUI.Sensors.PopUpWindowUtils.popup_field import Field


class DropdownField(Field):

    def __init__(self, options:List[str], functions:List, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        self.size = (self.size[0]-50, 0)

        if len(options) != len(functions):
            raise ValueError("Amount of options should be equal to amount of functions provided")

        self.options = options
        self.functions = functions

        self.curr_index = 0
        self.options_amount = len(options)

        def show_dropdown(button, *args):
            dp = DropDown()
            dp.bind(on_select=lambda instance, x: setattr(button, "text", x))
            for i in range(self.options_amount):
                item = Button(text=self.options[i], size_hint_y=None, height=44)
                item.bind(on_release=lambda btn: dp.select(btn.text))
                item.bind(on_release=lambda _: self.set_index(i))
                dp.add_widget(item)
            dp.open(button)

        self.button = Button()
        self.button.bind(on_release=show_dropdown)

        self.add_widget(self.button)
        self.set_index(self.curr_index)

    def set_index(self, index:int):
        self.button.text = self.options[index]
        self.functions[index](self.options[index])

    def update_value(self, value):
        if not type(value) == str:
            value = str(value)

        try:
            idx = self.options.index(value)
            self.set_index(idx)
        except ValueError:
            self.button.text = "Invalid option"



"""
        def show_dropdown(button, *largs):
            dp = DropDown()
            dp.bind(on_select=lambda instance, x: setattr(button, "text", x))
            for i in range(10):
                item = Button(text="hello %d" % i, size_hint_y=None, height=44)
                item.bind(on_release=lambda btn: dp.select(btn.text))
                dp.add_widget(item)
            dp.open(button)

        btn = Button(text="SHOW", size_hint=(None, None), pos=(300, 200))
        btn.bind(on_release=show_dropdown)

        boxlayout.add_widget(btn)
"""