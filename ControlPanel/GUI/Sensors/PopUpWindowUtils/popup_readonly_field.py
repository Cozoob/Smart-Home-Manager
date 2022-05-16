from kivy.uix.label import Label

from GUI.Sensors.PopUpWindowUtils.popup_field import Field


class ReadOnlyField(Field):
    def update_value(self, value):
        if not type(value) == str:
            value = str(value)
        self.value_label.text = value

    def __init__(self, field_name: str, **kwargs):
        super().__init__(**kwargs)

        self.field_name = field_name
        self.value_label = Label(text="no data...")

        self.orientation = "horizontal"
        self.add_widget(Label(text=self.field_name))
        self.add_widget(self.value_label)
