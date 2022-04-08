from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from GUI.Pages.scheme_page import SchemePage
from GUI.Pages.settings_page import SettingsPage
from GUI.Pages.home_page import HomePage

class MainLayout(TabbedPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_pos = 'top_mid'

        self.home_item = TabbedPanelItem(text="HOME")
        self.home_page = HomePage()
        self.home_item.add_widget(self.home_page)

        self.scheme_item = TabbedPanelItem(text="SCHEME")
        self.scheme_page = SchemePage()
        self.scheme_item.add_widget(self.scheme_page)

        self.settings_item = TabbedPanelItem(text="SETTINGS")
        self.settings_page = SettingsPage(self)
        self.settings_item.add_widget(self.settings_page)

        self.exit_item = TabbedPanelItem(text="EXIT",
                                         background_color='red',
                                         on_press=self.bye)

        self.add_widget(self.home_item)
        self.add_widget(self.scheme_item)
        self.add_widget(self.settings_item)
        self.add_widget(self.exit_item)

        self.default_tab = self.home_item

    def bye(self, *_):
        exit(0)

    def reload_settings(self):
        self.home_page.load()
        self.home_page.weather_widget.load()

    def reload_schema(self):
        pass