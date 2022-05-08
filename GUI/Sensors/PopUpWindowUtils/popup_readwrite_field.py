from abc import ABC

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from GUI.Sensors.PopUpWindowUtils.popup_field import Field
from GUI.Sensors.PopUpWindowUtils.validators import ValidatorAggregate, ValidatorInt, ValidatorFloat


class ReadWriteField(Field):

    def __init__(self, field_name: str, set_function=lambda x: ..., default_value="", **kwargs):
        super().__init__(**kwargs)

        self.validators = ValidatorAggregate()
        self.string_to_type_converter = lambda x: x

        self.set_function = set_function

        self.default_value = default_value

        def on_set(instance):
            value = self.string_to_type_converter(self.value_input.text)

            if not self.validators.isValid(value):
                print("Error")
                self.turn_invalid_state()
                return False

            self.set_function(value)
            self.update_value(value)

            print("Error on set: ", self.value_input.text)

        self.field_name = field_name
        self.value_input = TextInput(text=str(self.default_value), multiline=False, size_hint=(None, 1), size=(self.size[0]/2-50, 0))

        self.orientation = "horizontal"
        self.add_widget(Label(text=self.field_name, size_hint=(None, 1), size=(self.size[0]/2-50, 0)))
        self.add_widget(self.value_input)

        self.ok_button = Button(text="OK", size_hint=(None, 1), size=(50, 0))
        self.ok_button.bind(on_press=on_set)
        self.add_widget(self.ok_button)

        self.turn_valid_state()

    def update_value(self, value) -> bool:

        if not type(value) == str:
            value = str(value)
        self.value_input.text = value
        self.turn_valid_state()
        return True

    def turn_invalid_state(self):
        self.value_input.background_color = [1,0,0]

    def turn_valid_state(self):
        self.value_input.background_color = [1,1,1]


class ReadWriteFieldInt(ReadWriteField):

    def __init__(self, field_name:str, set_function, min_val:int, max_val:int, **kwargs):
        super().__init__(field_name, set_function, **kwargs)

        self.validators.add_validator(ValidatorInt(min_val, max_val))
        self.string_to_type_converter = ReadWriteFieldInt.string_to_type_converter_fun

    @classmethod
    def string_to_type_converter_fun(cls, x:str):
        try:
            value = int(x)
        except ValueError:
            value = 0

        return value


class ReadWriteFieldFloat(ReadWriteField):

    def __init__(self, field_name: str, **kwargs):
        super().__init__(field_name, **kwargs)

        self.validators.add_validator(ValidatorFloat(0, 1))
        self.string_to_type_converter = ReadWriteFieldFloat.string_to_type_converter_fun

    @classmethod
    def string_to_type_converter_fun(cls, x: str):
        try:
            value = float(x)
        except ValueError:
            value = 0

        return value
