from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import OptionProperty
from kivy import require

require('2.1.0')


class MainApp(App):
    def build(self):
        return MainLayout()
        # return self.navbar

class MainLayout(TabbedPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_pos = 'top_mid'

        self.scheme_item = TabbedPanelItem(text="SCHEME")
        self.scheme_page = SchemePage()
        self.scheme_item.add_widget(self.scheme_page)

        self.settings_item = TabbedPanelItem(text="SETTINGS")
        self.settings_page = SettingsPage()
        self.settings_item.add_widget(self.settings_page)

        self.exit_item = TabbedPanelItem(text="EXIT",
                                         background_color='red',
                                         on_press=self.bye)

        self.add_widget(self.scheme_item)
        self.add_widget(self.settings_item)
        self.add_widget(self.exit_item)

    def bye(self, *_):
        exit(0)


class SchemePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1
        # self.message = Label(halign="center", valign="middle", font_size=18)
        # self.message.bind(width=self.update_text_width)
        # self.add_widget(self.message)

        self.add_widget(Label(text="TEXT"))

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)


class SettingsPage(GridLayout):
    pass

# class Pages(PageLayout):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.button1 = Button(text='page1')
#         self.columns = 2
#
#
#
#     pass



if __name__ == '__main__':
    app = MainApp()
    app.run()
