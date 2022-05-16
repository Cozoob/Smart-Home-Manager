from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# from GUI.main_layout import MainLayout

import json


class SettingsPage(RelativeLayout):
    first_name = "NN"
    last_name = "NN"
    country = "NN"
    region = "NN"
    city = "NN"
    API_key = "NN"
    broker_ip = "127.0.0.1"
    broker_port = 8080

    inp_first_name = TextInput(text=f"{first_name}")
    inp_last_name = TextInput(text=f"{last_name}")
    inp_country = TextInput(text=f"{country}")
    inp_region = TextInput(text=f"{region}")
    inp_city = TextInput(text=f"{city}")
    inp_api_key = TextInput(text=f"{API_key}", multiline=False)
    inp_broker_ip = TextInput(text=f"{broker_ip}", multiline=False)
    inp_broker_port = TextInput(text=f"{broker_port}", multiline=False)

    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 9

        self.data = []

        self.main_layout = main_layout

        self.create_layout()

    def load_data(self):

        try:
            with open("./Data/user.json", "r") as file:
                data = json.loads(file.read())
                self.data = data

                self.first_name = data["first_name"]
                self.last_name = data["last_name"]
                self.country = data["country"]
                self.region = data["region"]
                self.city = data["city"]
                self.API_key = data["API_key"]
                self.broker_ip = data["Broker_IP"]
                self.broker_port = data["Broker_Port"]

                self.inp_first_name = TextInput(text=f"{self.first_name}")
                self.inp_last_name = TextInput(text=f"{self.last_name}")
                self.inp_country = TextInput(text=f"{self.country}")
                self.inp_region = TextInput(text=f"{self.region}")
                self.inp_city = TextInput(text=f"{self.city}")
                self.inp_api_key = TextInput(text=f"{self.API_key}", multiline=False)
                self.inp_broker_ip = TextInput(
                    text=f"{self.broker_ip}", multiline=False
                )
                self.inp_broker_port = TextInput(
                    text=f"{self.broker_port}", multiline=False
                )

        except FileNotFoundError:
            pass

    def create_layout(self):
        self.load_data()

        # First name
        grid_first_name = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.20, 0.125),
            pos_hint={"top": 0.9, "x": 0.38},
        )

        lbl_first_name = Label(text="First name")
        grid_first_name.add_widget(lbl_first_name)

        grid_first_name.add_widget(self.inp_first_name)

        self.add_widget(grid_first_name)

        # Last name
        grid_last_name = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.20, 0.125),
            pos_hint={"top": 0.85, "x": 0.38},
        )

        lbl_last_name = Label(text="Last name")
        grid_last_name.add_widget(lbl_last_name)

        grid_last_name.add_widget(self.inp_last_name)

        self.add_widget(grid_last_name)

        # Country
        grid_country = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.20, 0.125),
            pos_hint={"top": 0.80, "x": 0.38},
        )

        lbl_country = Label(text="Country")
        grid_country.add_widget(lbl_country)

        grid_country.add_widget(self.inp_country)

        self.add_widget(grid_country)

        # Region
        grid_region = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.20, 0.125),
            pos_hint={"top": 0.75, "x": 0.38},
        )

        lbl_region = Label(text="Region")
        grid_region.add_widget(lbl_region)

        grid_region.add_widget(self.inp_region)

        self.add_widget(grid_region)

        # City
        grid_city = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.20, 0.125),
            pos_hint={"top": 0.70, "x": 0.38},
        )

        lbl_city = Label(text="City")
        grid_city.add_widget(lbl_city)

        grid_city.add_widget(self.inp_city)

        self.add_widget(grid_city)

        # API KEY
        grid_api_key = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.28, 0.125),
            pos_hint={"top": 0.65, "x": 0.34},
        )

        lbl_api_key = Label(text="API key")
        grid_api_key.add_widget(lbl_api_key)

        grid_api_key.add_widget(self.inp_api_key)

        self.add_widget(grid_api_key)

        # BROKER IP
        grid_broker_ip = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.28, 0.125),
            pos_hint={"top": 0.60, "x": 0.34},
        )

        lbl_broker_ip = Label(text="Broker IP")
        grid_broker_ip.add_widget(lbl_broker_ip)

        grid_broker_ip.add_widget(self.inp_broker_ip)

        self.add_widget(grid_broker_ip)

        # BROKER PORT
        grid_broker_port = GridLayout(
            cols=2,
            rows=1,
            row_force_default=True,
            row_default_height=40,
            size_hint=(0.28, 0.125),
            pos_hint={"top": 0.55, "x": 0.34},
        )

        lbl_broker_port = Label(text="Broker port")
        grid_broker_port.add_widget(lbl_broker_port)

        grid_broker_port.add_widget(self.inp_broker_port)

        self.add_widget(grid_broker_port)

        # Save button
        submit_button = Button(
            text="Save",
            on_press=self.save_changes,
            size_hint=(0.10, 0.10),
            pos_hint={"top": 0.15, "x": 0.45},
        )
        self.add_widget(submit_button)

    def save_changes(self, instance):
        print(f"The user data has been saved.")

        self.data["first_name"] = self.inp_first_name.text
        self.data["last_name"] = self.inp_last_name.text
        self.data["country"] = self.inp_country.text
        self.data["region"] = self.inp_region.text
        self.data["city"] = self.inp_city.text
        self.data["API_key"] = self.inp_api_key.text
        self.data["Broker_IP"] = self.inp_broker_ip.text
        self.data["Broker_Port"] = self.inp_broker_port.text

        try:
            with open("./Data/user.json", "w") as file:
                json.dump(self.data, file)
        except FileNotFoundError:
            print("Cannot save changes.")

        self.main_layout.reload_settings()
