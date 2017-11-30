from settings import TEST_ENVIRONMENT


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, StringProperty

import time

if not TEST_ENVIRONMENT:
    from data_with_write import HX711
    from Adafruit_BNO055 import BNO055


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

    # 1 / 3 of arrow height and width
    arrow_height = 5
    arrow_width = 5
    forward_arrow_color = ListProperty()
    backward_arrow_color = ListProperty()
    left_arrow_color = ListProperty()
    right_arrow_color = ListProperty()

    def __init__(self, **kwargs):
        super(SmartWalker, self).__init__(**kwargs)
        self.min = -500
        self.max = 500
        self.ellipse_color_gy = 1, 1, 1, 1
        self.forward_arrow_color = 1, 1, 1, 1
        self.backward_arrow_color = 0, 1, 1, 1
        self.left_arrow_color = 1, 0, 1, 1
        self.right_arrow_color = 1, 1, 0, 1

        if not TEST_ENVIRONMENT:
            self.hx0 = HX711(27, 17)
            self.hx1 = HX711(10, 22)
            self.hx2 = HX711(11, 9)
            self.hx3 = HX711(26, 13)

            self.initialize_weight_sensor(self.hx0)
            self.initialize_weight_sensor(self.hx1)
            self.initialize_weight_sensor(self.hx2)
            self.initialize_weight_sensor(self.hx3)

            self.bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=23)

            if not self.bno.begin():
                raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    def initialize_weight_sensor(self, sensor):
        sensor.set_reading_format("LSB", "MSB")
        sensor.set_reference_unit(92)
        sensor.reset()
        sensor.tare()

    def get_4_weight_sensors(self):
        if TEST_ENVIRONMENT:
            return 100, 100, 100, 100
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

            return val0, val1, val2, val3

        except (KeyboardInterrupt, SystemExit):
            self.hx0.cleanAndExit()
            self.hx1.cleanAndExit()
            self.hx2.cleanAndExit()
            self.hx3.cleanAndExit()
            return 1, 1, 1, 1

    def update_weights(self):
        self.sensors = self.get_4_weight_sensors()
        self.rr_text = str(self.sensors[0])
        self.fr_text = str(self.sensors[1])
        self.rl_text = str(self.sensors[2])
        self.fl_text = str(self.sensors[3])
        self.change_color()

    def update_gyroscope(self):
        if not TEST_ENVIRONMENT:
            heading, roll, pitch = self.bno.read_euler()
            sys, gyro, acc, mag = self.bno.get_calibration_status()
        else:
            heading, roll, pitch = 100, 45, 30
            sys, gyro, acc, mag = 20, 12, 10, 4

        if roll < -40:
            self.forward_arrow_color = 1, 0, 0, 1
        else:
            self.forward_arrow_color = 0, 1, 0, 1
        if roll > 40:
            self.backward_arrow_color = 1, 0, 0, 1
        else:
            self.backward_arrow_color = 0, 1, 0, 1

        self.left_arrow_color = 0, 1, 0, 1
        self.right_arrow_color = 0, 1, 0, 1

        self.bno_heading = str(heading)
        self.bno_roll = str(roll)
        self.bno_pitch = str(pitch)
        self.bno_sys = str(sys)
        self.bno_gyro = str(gyro)
        self.bno_acc = str(acc)
        self.bno_mag = str(mag)

    def update(self, *args):
        self.thisTime = str(time.asctime())
        self.update_weights()
        self.update_gyroscope()

    def change_color(self):
        self.ellipse_color_fl = self.get_color(self.sensors[3])
        self.ellipse_color_fr = self.get_color(self.sensors[1])
        self.ellipse_color_rl = self.get_color(self.sensors[2])
        self.ellipse_color_rr = self.get_color(self.sensors[0])

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
        return r / 255., g / 255., b / 255., 1


class SmartApp(App):
    def build(self):
        s = SmartWalker()
        # Clock.schedule_interval(s.update, 10)
        return s


if __name__ == '__main__':
    SmartApp().run()
