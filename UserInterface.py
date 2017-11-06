from kivy.app import App
from kivy.uix.widget import Widget

class SmartWalker(Widget):
    pass


class SmartApp(App):
    def build(self):
        return SmartWalker()


if __name__ == '__main__':
    SmartApp().run()
