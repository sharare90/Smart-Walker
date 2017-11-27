from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
import time
from data_with_write import HX711
from Adafruit_BNO055 import BNO055
from kivy.properties import ListProperty, ObjectProperty, StringProperty


class SmartWalker(Widget):
    front_left_leg = ObjectProperty()
    front_right_leg = ObjectProperty()
    rear_left_leg = ObjectProperty()
    rear_right_leg = ObjectProperty()
    ellipse_color_fl = ListProperty()
    ellipse_color_fr = ListProperty()
    ellipse_color_rl = ListProperty()
    ellipse_color_rr = ListProperty()
    ellipse_color_gy = ListProperty()
    thisTime = StringProperty("")

    sensors = ListProperty()
    fl_text = StringProperty("")
    fr_text = StringProperty("")
    rl_text = StringProperty("")
    rr_text = StringProperty("")

    bno_heading = StringProperty("")
    bno_roll = StringProperty("")
    bno_pitch = StringProperty("")
    bno_sys = StringProperty("")
    bno_gyro = StringProperty("")
    bno_acc = StringProperty("")
    bno_mag = StringProperty("")

    def __init__(self, **kwargs):
        super(SmartWalker, self).__init__(**kwargs)
        self.hx0 = HX711(27, 17)
        self.hx1 = HX711(10, 22)
        self.hx2 = HX711(11, 9)
        self.hx3 = HX711(26, 13)

        self.hx0.set_reading_format("LSB", "MSB")
        self.hx0.set_reference_unit(92)
        self.hx0.reset()
        self.hx0.tare()

        self.hx1.set_reading_format("LSB", "MSB")
        self.hx1.set_reference_unit(92)
        self.hx1.reset()
        self.hx1.tare()

        self.hx2.set_reading_format("LSB", "MSB")
        self.hx2.set_reference_unit(92)
        self.hx2.reset()
        self.hx2.tare()

        self.hx3.set_reading_format("LSB", "MSB")
        self.hx3.set_reference_unit(92)
        self.hx3.reset()
        self.hx3.tare()
        self.min = -500
        self.max = 500

        self.bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=23)

        if not self.bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    def get_4_weight_sensors(self):
        # self.val0 = 0  # rr
        # self.val1 = 0  # fr
        # self.val2 = 0  # rl
        # self.val3 = 0  # fl

        try:
            self.hx0.power_down()
            self.hx0.power_up()

            self.hx1.power_down()
            self.hx1.power_up()

            self.hx2.power_down()
            self.hx2.power_up()

            self.hx3.power_down()
            self.hx3.power_up()

            val0 = self.hx0.get_weight(5)
            val1 = self.hx1.get_weight(5)
            val2 = self.hx2.get_weight(5)
            val3 = self.hx3.get_weight(5)
            # print self.val0, ",", self.val1, ",", self.val2, ",", self.val3
            return val0, val1, val2, val3
        except (KeyboardInterrupt, SystemExit):
            self.hx0.cleanAndExit()
            self.hx1.cleanAndExit()
            self.hx2.cleanAndExit()
            self.hx3.cleanAndExit()

    def update(self, *args):
        self.thisTime = str(time.asctime())
        self.sensors = self.get_4_weight_sensors()
        # sensors = [4, 5, 6, 7]
        self.rr_text = str(self.sensors[0])
        self.fr_text = str(self.sensors[1])
        self.rl_text = str(self.sensors[2])
        self.fl_text = str(self.sensors[3])
        self.change_color()

        heading, roll, pitch = self.bno.read_euler()
        sys, gyro, acc, mag = self.bno.get_calibration_status()
        self.bno_heading = str(heading)
        self.bno_roll = str(roll)
        self.bno_pitch = str(pitch)
        self.bno_sys = str(sys)
        self.bno_gyro = str(gyro)
        self.bno_acc = str(acc)
        self.bno_mag = str(mag)
        # print(
        # 'Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
        #     heading, roll, pitch, sys, gyro, acc, mag))

    def change_color(self):
        self.ellipse_color_fl = self.get_color(self.sensors[3])
        self.ellipse_color_fr = self.get_color(self.sensors[1])
        self.ellipse_color_rl = self.get_color(self.sensors[2])
        self.ellipse_color_rr = self.get_color(self.sensors[0])
        # self.ellipse_color_fl = 0, 1, 0, 1
        # self.ellipse_color_fr = 0, 1, 0, 1
        # self.ellipse_color_rl = 0, 1, 0, 1
        # self.ellipse_color_rr = 0, 1, 0, 1
        # if self.sensors[3] > 100:
        #     self.ellipse_color_fl = 1, 0, 0, 1
        # if self.sensors[1] > 100:
        #     self.ellipse_color_fr = 1, 0, 0, 1
        # if self.sensors[2] > 100:
        #     self.ellipse_color_rl = 1, 0, 0, 1
        # if self.sensors[0] > 100:
        #     self.ellipse_color_rr = 1, 0, 0, 1

    def get_color(self, value):
        minimum, maximum = float(self.min), float(self.max)
        if value < minimum:
            value = minimum
        elif value > maximum:
            value = maximum

        ratio = 2 * (value - minimum) / (maximum - minimum)
        b = int(max(0, 255 * (1 - ratio)))
        r = int(max(0, 255 * (ratio - 1)))
        g = 255 - b - r
        return r, g, b, 1


class SmartApp(App):
    def build(self):
        s = SmartWalker()
        Clock.schedule_interval(s.update, 1)
        return s


if __name__ == '__main__':
    SmartApp().run()
