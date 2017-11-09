from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ListProperty, ObjectProperty


class SmartWalker(Widget):
    front_left_leg = ObjectProperty()
    ellipse_color_fl = ListProperty([1, 0, 0, 1])
    ellipse_color_fr = ListProperty([1, 0, 0, 1])
    ellipse_color_rl = ListProperty([1, 0, 0, 1])
    ellipse_color_rr = ListProperty([1, 0, 0, 1])
    ellipse_color_gy = ListProperty([1, 0, 0, 1])

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
        return SmartWalker()


if __name__ == '__main__':
    SmartApp().run()
