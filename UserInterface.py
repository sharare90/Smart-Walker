from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
import time
from kivy.properties import ListProperty, ObjectProperty, StringProperty


class SmartWalker(Widget):
    front_left_leg = ObjectProperty()
    front_right_leg = ObjectProperty()
    rear_left_leg = ObjectProperty()
    rear_right_leg = ObjectProperty()
    ellipse_color_fl = ListProperty([1, 0, 0, 1])
    ellipse_color_fr = ListProperty([1, 0, 0, 1])
    ellipse_color_rl = ListProperty([1, 0, 0, 1])
    ellipse_color_rr = ListProperty([1, 0, 0, 1])
    ellipse_color_gy = ListProperty([1, 0, 0, 1])
    timer = ObjectProperty()
    thisTime = StringProperty("")

    def update(self, *args):
        self.thisTime = str(time.asctime())

    def change_color(self, leg):
        if leg == self.front_left_leg:
            self.ellipse_color_fl = 1, 1, 1, 1
        if leg == self.front_right_leg:
            self.ellipse_color_fr = 1, 1, 1, 1
        if leg == self.rear_left_leg:
            self.ellipse_color_rl = 1, 1, 1, 1
        if leg == self.rear_right_leg:
            self.ellipse_color_rr = 1, 1, 1, 1


class SmartApp(App):
    def build(self):
        s = SmartWalker()
        Clock.schedule_interval(s.update, 1)
        return s


if __name__ == '__main__':
    SmartApp().run()
