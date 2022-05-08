from typing import List

from kivy.uix.button import Button

from GUI.Sensors.PopUpWindowUtils.popup_field import Field


class CycleField(Field):

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

        self.button = Button()
        self.add_widget(self.button)

        def next_option(instance):
            self.curr_index += 1
            self.curr_index %= self.options_amount

            self.change_index(self.curr_index)

        self.button.bind(on_press=next_option)

        self.set_index(self.curr_index)

    def change_index(self, index:int):
        self.button.text = self.options[index]
        self.functions[index]()
        self.curr_index = index

    def set_index(self, index:int):
        self.button.text = self.options[index]
        self.curr_index = index

    def update_value(self, value):
        if not type(value) == str:
            value = str(value)

        try:
            idx = self.options.index(value)
            self.set_index(idx)
        except ValueError:
            self.button.text = "Invalid option"
