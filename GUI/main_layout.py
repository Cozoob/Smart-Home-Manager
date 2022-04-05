from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from GUI.Pages.scheme_page import SchemePage
from GUI.Pages.settings_page import SettingsPage

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

        self.default_tab = self.scheme_item

    def bye(self, *_):
        exit(0)