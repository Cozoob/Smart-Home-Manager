from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# from GUI.main_layout import MainLayout

import json

class SettingsPage(RelativeLayout):

    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 7

        self.data = []

        self.main_layout = main_layout

        self.first_name = 'NN'
        self.last_name = 'NN'
        self.country = 'NN'
        self.region = 'NN'
        self.city = 'NN'
        self.API_key = 'NN'

        self.inp_first_name = TextInput(text=f"{self.first_name}")
        self.inp_last_name = TextInput(text=f"{self.last_name}")
        self.inp_country = TextInput(text=f"{self.country}")
        self.inp_region = TextInput(text=f"{self.region}")
        self.inp_city = TextInput(text=f"{self.city}")
        self.inp_api_key = TextInput(text=f"{self.API_key}", multiline=False)

        self.create_layout()


    def load_data(self):

        try:
            with open('./Data/user.json', 'r') as file:
                data = json.loads(file.read())
                self.data = data

                self.first_name = data['first_name']
                self.last_name = data['last_name']
                self.country = data['country']
                self.region = data['region']
                self.city = data['city']
                self.API_key = data['API_key']

                self.inp_first_name = TextInput(text=f"{self.first_name}")
                self.inp_last_name = TextInput(text=f"{self.last_name}")
                self.inp_country = TextInput(text=f"{self.country}")
                self.inp_region = TextInput(text=f"{self.region}")
                self.inp_city = TextInput(text=f"{self.city}")
                self.inp_api_key = TextInput(text=f"{self.API_key}", multiline=False)

        except FileNotFoundError:
            pass



    def create_layout(self):
        self.load_data()

        # First name
        grid_first_name = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=40,
                           size_hint=(0.20, 0.125), pos_hint={'top': 0.9, 'x': 0.38})

        lbl_first_name = Label(text="First name")
        grid_first_name.add_widget(lbl_first_name)

        grid_first_name.add_widget(self.inp_first_name)

        self.add_widget(grid_first_name)

        # Last name
        grid_last_name = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=40,
                           size_hint=(0.20, 0.125), pos_hint={'top': 0.85, 'x': 0.38})

        lbl_last_name = Label(text="Last name")
        grid_last_name.add_widget(lbl_last_name)

        grid_last_name.add_widget(self.inp_last_name)

        self.add_widget(grid_last_name)

        # Country
        grid_country = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=40,
                                    size_hint=(0.20, 0.125), pos_hint={'top': 0.80, 'x': 0.38})

        lbl_country = Label(text="Country")
        grid_country.add_widget(lbl_country)

        grid_country.add_widget(self.inp_country)

        self.add_widget(grid_country)

        # Region
        grid_region = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=40,
                                    size_hint=(0.20, 0.125), pos_hint={'top': 0.75, 'x': 0.38})

        lbl_region = Label(text="Region")
        grid_region.add_widget(lbl_region)

        grid_region.add_widget(self.inp_region)

        self.add_widget(grid_region)

        # City
        grid_city = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=40,
                                    size_hint=(0.20, 0.125), pos_hint={'top': 0.70, 'x': 0.38})

        lbl_city = Label(text="City")
        grid_city.add_widget(lbl_city)

        grid_city.add_widget(self.inp_city)

        self.add_widget(grid_city)

        # API KEY
        grid_api_key = GridLayout(cols=2, rows=1, row_force_default=True, row_default_height=40,
                                    size_hint=(0.28, 0.125), pos_hint={'top': 0.65, 'x': 0.34})

        lbl_api_key = Label(text="API key")
        grid_api_key.add_widget(lbl_api_key)

        grid_api_key.add_widget(self.inp_api_key)

        self.add_widget(grid_api_key)

        # Save button
        submit_button = Button(text="Save", on_press=self.save_changes, size_hint=(0.10, 0.10),
                               pos_hint={'top': 0.15, 'x': 0.45})
        self.add_widget(submit_button)

    def save_changes(self, instance):
        print(f"The user data has been saved.")

        self.data['first_name'] = self.inp_first_name.text
        self.data['last_name'] = self.inp_last_name.text
        self.data['country'] = self.inp_country.text
        self.data['region'] = self.inp_region.text
        self.data['city'] = self.inp_city.text
        self.data['API_key'] = self.inp_api_key.text

        try:
            with open("./Data/user.json", "w") as file:
                json.dump(self.data, file)
        except FileNotFoundError:
            print("Cannot save changes.")

        self.main_layout.reload_settings()