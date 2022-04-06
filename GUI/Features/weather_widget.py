
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
import urllib.request
import json
from time import gmtime, strftime
from kivy.network.urlrequest import UrlRequest


class WeatherBoxWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(WeatherWidget())


class WeatherWidget(RelativeLayout):
    """
    Shows the current weather and 5 day forecast based on OpenWeatherMap API.
    """

    city = StringProperty('--')
    country = StringProperty('--')
    temperature = StringProperty('--')
    humidity = StringProperty('--')
    pressure = StringProperty('--')
    image = StringProperty('--')
    wind_speed = StringProperty('--')
    wind_direction = StringProperty('--')
    last_update = StringProperty('--')
    notification = StringProperty('')
    image_source = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 3

        self.size = (10, 10)

        try:
            with open('./Data/user.json', 'r') as file:
                user_info = json.loads(file.read())
        except FileNotFoundError:
            pass

        self.API_key = user_info['API_key']
        city = user_info['city']

        self.download_current_weather(city=f"{city}")



    def download_current_weather(self, city, *args, **kwargs):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + f'&APPID={self.API_key}'
        UrlRequest(url=url, on_success=self.show_current_weather, on_error=self.download_error, on_progress=self.progress,
                   chunk_size=40960)


    def download_error(self, request, error):
        """
        Notifies on error
        """
        self.notification = 'data could not be downloaded' + error
        print(self.notification)


    def progress(self, request, current_size, total_size):
        """
        Shows progress to the user
        """
        self.notification = ('Downloading data: {} bytes of {} bytes'.format(current_size, total_size))
        print(self.notification)


    def show_current_weather(self, request, result):

        self.city = result.get('name', 'nn')
        self.country = result.get('sys').get('country', 'nn')
        self.temperature = '{:.0f}'.format(result.get('main').get('temp') - 273.15)
        self.humidity = str(result.get('main').get('humidity', 'nn'))
        self.pressure = str(result.get('main').get('pressure', 'nn'))
        self.image_source = 'http://openweathermap.org/img/w/' + result['weather'][0]['icon'] + '.png'
        self.wind_speed = str(result.get('wind').get('speed', 'nn'))
        self.wind_direction = str(result.get('wind').get('deg', 'nn'))
        self.last_update = str(gmtime(result.get('dt')))

        self.notification = ''

        self.clear_widgets()

        # Add labels
        lbl1 = Label(text=f"{self.city}" + ", " + f"{self.country}", font_size=40, size_hint=(1, .25),
                     pos_hint={'top': 1, 'left': 1})
        self.add_widget(lbl1)

        img1 = AsyncImage(source=self.image_source, allow_stretch=True, keep_ratio=True, size_hint=(0.25, 0.25),
                          pos_hint={'top': 0.75, 'left': 0.1})
        self.add_widget(img1)

        lbl2 = Label(text=f"{self.temperature}" + u" \xb0C", font_size=40, size_hint=(0.25, 0.25),
                     pos_hint={'top': 0.75, 'x': 0.25})
        self.add_widget(lbl2)

        lbl3 = Label(text=f"{self.humidity}" + " %rH", font_size=20, size_hint=(0.25, 0.125),
                     pos_hint={'top': 0.75, 'x': 0.5})
        self.add_widget(lbl3)

        lbl4 = Label(text=f"{self.pressure}" + " hPa", font_size=20, size_hint=(0.25, 0.125),
                     pos_hint={'top': 0.75, 'x': 0.75})
        self.add_widget(lbl4)

        lbl5 = Label(text=f"{self.wind_speed}" + " m/s", font_size=20, size_hint=(0.25, 0.125),
                     pos_hint={'top': 0.625, 'x': 0.5})
        self.add_widget(lbl5)

        lbl6 = Label(text=f"{self.wind_direction}" + u" \xb0", font_size=20, size_hint=(0.25, 0.125),
                     pos_hint={'top': 0.625, 'x': 0.75})
        self.add_widget(lbl6)
