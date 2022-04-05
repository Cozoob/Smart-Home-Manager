from GUI.main_layout import MainLayout

from kivy.app import App
from kivy import require

require('2.1.0')

class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    app = MainApp()
    app.run()
