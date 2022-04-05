from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

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