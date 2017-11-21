from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
import time
from data_with_write import HX711
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
    thisTime = StringProperty("")
    fl_text = StringProperty("")
    fr_text = StringProperty("")
    rl_text = StringProperty("")
    rr_text = StringProperty("")

    @staticmethod
    def get_4_weight_sensors():
        # self.val0 = 0  # rr
        # self.val1 = 0  # fr
        # self.val2 = 0  # rl
        # self.val3 = 0  # fl
        hx0 = HX711(27, 17, 128)
        hx1 = HX711(10, 22, 128)
        hx2 = HX711(11, 9, 128)
        hx3 = HX711(26, 13, 128)

        hx0.set_reading_format("LSB", "MSB")
        hx0.set_reference_unit(92)
        hx0.reset()
        hx0.tare()

        hx1.set_reading_format("LSB", "MSB")
        hx1.set_reference_unit(92)
        hx1.reset()
        hx1.tare()

        hx2.set_reading_format("LSB", "MSB")
        hx2.set_reference_unit(92)
        hx2.reset()
        hx2.tare()

        hx3.set_reading_format("LSB", "MSB")
        hx3.set_reference_unit(92)
        hx3.reset()
        hx3.tare()

        try:
            hx0.power_down()
            hx0.power_up()

            hx1.power_down()
            hx1.power_up()

            hx2.power_down()
            hx2.power_up()

            hx3.power_down()
            hx3.power_up()

            val0 = hx0.get_weight(5)
            val1 = hx1.get_weight(5)
            val2 = hx2.get_weight(5)
            val3 = hx3.get_weight(5)
            # print self.val0, ",", self.val1, ",", self.val2, ",", self.val3
            return val0, val1, val2, val3
        except (KeyboardInterrupt, SystemExit):
            hx0.cleanAndExit()
            hx1.cleanAndExit()
            hx2.cleanAndExit()
            hx3.cleanAndExit()

    def update(self, *args):
        self.thisTime = str(time.asctime())
        # sensors = self.get_4_weight_sensors()
        sensors = [4, 5, 6, 7]
        self.rr_text = str(sensors[0])
        self.fr_text = str(sensors[1])
        self.rl_text = str(sensors[2])
        self.fl_text = str(sensors[3])

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
