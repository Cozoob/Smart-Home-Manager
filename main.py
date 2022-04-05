from GUI.main_layout import MainLayout
from kivy.app import App
from kivy.core.window import Window

from kivy import require
require('2.1.0')

class MainApp(App):
    def build(self):
        Window.size = (1280, 720)
        Window.maximize()
        return MainLayout()


if __name__ == '__main__':
    app = MainApp()
    app.run()
