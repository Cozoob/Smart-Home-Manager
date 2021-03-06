import json

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from GUI.Features.weather_widget import WeatherBoxWidget


def load_name() -> str:
    # in the future loading from json
    name = "NOT FOUND"
    try:
        with open("./Data/user.json", "r") as file:
            user = json.loads(file.read())
            name = user["first_name"]
    except FileNotFoundError:
        pass

    return name


class HomePage(GridLayout):

    user = StringProperty("--")
    hello_message = StringProperty("--")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3

        self.homepage_text = Label(text="HOMEPAGE", font_size=60, height=100)

        self.weather_widget = WeatherBoxWidget()

        self.load()

        Clock.schedule_interval(lambda _: self.weather_widget.load(), 60)

    def load(self):
        print("Loading user name in home page.")
        self.user = load_name()
        self.hello_message = f"Welcome {self.user}!"

        self.clear_widgets()

        user = load_name()
        hello_message = f"Welcome {user}!"
        hello_text = Label(text=hello_message, font_size=50, height=100)

        self.add_widget(self.homepage_text)
        self.add_widget(hello_text)
        self.add_widget(self.weather_widget)
