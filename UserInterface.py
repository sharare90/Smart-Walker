from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line

from smart_walker_exceptions import NoDrPrescriptionFound
from settings import TEST_ENVIRONMENT

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty, BooleanProperty

from logger import Logger, DataSources

import time
import random

if not TEST_ENVIRONMENT:
    from weight_sensor import WeightSensor
    from Adafruit_BNO055 import BNO055
    from Dependencies.VL53L0X_rasp_python.python.VL53L0X import VL53L0X
    from Dependencies.VL53L0X_rasp_python.python.VL53L0X import VL53L0X_BETTER_ACCURACY_MODE


class SmartWalker(Widget):
    time = StringProperty("")
    safe = BooleanProperty(True)

    # 1 / 3 of arrow height and width
    arrow_height = 5
    arrow_width = 5
    forward_arrow_color = ListProperty()
    backward_arrow_color = ListProperty()
    left_arrow_color = ListProperty()
    right_arrow_color = ListProperty()

    def __init__(self, **kwargs):
        super(SmartWalker, self).__init__(**kwargs)
        self.set_dr_prescription()
        self.logger = Logger()

        self.forward_arrow_color = 1, 1, 1, 1
        self.backward_arrow_color = 0, 1, 1, 1
        self.left_arrow_color = 1, 0, 1, 1
        self.right_arrow_color = 1, 1, 0, 1

        if not TEST_ENVIRONMENT:
            self.hx0 = WeightSensor(27, 17)
            self.hx3 = WeightSensor(26, 13)
            self.hx1 = WeightSensor(10, 22)
            self.hx2 = WeightSensor(11, 9)

            self.hx0.initialize_weight_sensor()
            self.hx1.initialize_weight_sensor()
            self.hx2.initialize_weight_sensor()
            self.hx3.initialize_weight_sensor()

            self.bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=23)
            heading, roll, pitch = self.bno.read_euler()
            self.gyro.set_initial_values(heading, roll, pitch)

            if not self.bno.begin():
                raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

            self.tof = VL53L0X()
            self.tof.start_ranging(VL53L0X_BETTER_ACCURACY_MODE)

        else:
            heading, roll, pitch = 100, random.uniform(0, 0.1), random.uniform(0, 0.1)
            self.gyro.set_initial_values(heading, roll, pitch)

    def set_dr_prescription(self):
        try:
            with open('dr_note.txt') as f:
                numbers = map(float, f.readline().split(' '))
        except:
            raise NoDrPrescriptionFound()

        if numbers:
            PressureSensorWidget.set_max_dr_value(max(numbers[:4]))

            self.fl.set_dr_radius(numbers[0])
            self.fr.set_dr_radius(numbers[1])
            self.rl.set_dr_radius(numbers[2])
            self.rr.set_dr_radius(numbers[3])
            ProximityWidget.set_dr_value(int(numbers[4]))

    def get_4_weight_sensors(self):
        """returns rr, fr, rl, fl,
         calibration values: 6.1324866, 4.3640498, 4.50525366, 4.35680998 """
        if TEST_ENVIRONMENT:
            import random
            return random.randrange(10000) - 9000, random.randrange(10000) - 5000, random.randrange(
                10000) - 5000, random.randrange(10000) - 5000
        try:
            val0 = self.hx0.get_weight(1)
            val1 = self.hx1.get_weight(1)
            val2 = self.hx2.get_weight(1)
            val3 = self.hx3.get_weight(1)

            calibrated_val0 = 6.1324866 * val0 / 1000
            calibrated_val1 = 4.3640498 * val1 / 1000
            calibrated_val2 = 4.50525366 * val2 / 1000
            calibrated_val3 = 4.35680998 * val3 / 1000

            return calibrated_val0, calibrated_val1, calibrated_val2, calibrated_val3

        except (KeyboardInterrupt, SystemExit):
            self.hx0.cleanAndExit()
            self.hx1.cleanAndExit()
            self.hx2.cleanAndExit()
            self.hx3.cleanAndExit()
            return 1, 1, 1, 1

    def update_weights(self):
        rr_value, fr_value, rl_value, fl_value = self.get_4_weight_sensors()
        self.logger.add_data([fr_value, fl_value, rr_value, rl_value], DataSources.WEIGHT)
        self.rr.set_pressure(rr_value)
        self.fr.set_pressure(fr_value)
        self.rl.set_pressure(rl_value)
        self.fl.set_pressure(fl_value)

    def update_gyroscope(self):
        if not TEST_ENVIRONMENT:
            heading, roll, pitch = self.bno.read_euler()
            sys, gyro, acc, mag = self.bno.get_calibration_status()
        else:
            heading, roll, pitch = 100, random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)
            sys, gyro, acc, mag = 20, 12, 10, 4

        self.logger.add_data([heading, roll, pitch, sys, gyro, acc, mag], DataSources.GYROSCOPE)
        self.gyro.set_roll_pos(roll)
        self.gyro.set_pitch_pos(pitch)

        if roll < -40:
            self.forward_arrow_color = 1, 0, 0, 1
        else:
            self.forward_arrow_color = 0, 1, 0, 1
        if roll > 40:
            self.backward_arrow_color = 1, 0, 0, 1
        else:
            self.backward_arrow_color = 0, 1, 0, 1

    def update_proximity(self):
        if not TEST_ENVIRONMENT:
            proximity_value = self.tof.get_distance()
        else:
            import random
            proximity_value = random.randrange(1000)

        self.logger.add_data([proximity_value], DataSources.PROXIMITY)
        self.proximity.set_proximity(proximity_value)

    def update_safe(self, *args):
        self.safe = random.uniform(0, 1) < 0.6

    def update(self, *args):
        self.time = str(time.asctime())
        self.update_weights()
        self.update_gyroscope()
        self.update_proximity()
        self.logger.write_data_to_file()
        # self.logger.capture_photos()


class GyroWidget(Widget):
    max_pitch_value = 170
    min_pitch_value = 160
    max_roll_value = -73
    min_roll_value = -83
    # max_pitch_value = 0.1
    # min_pitch_value = -0.1
    # max_roll_value = 0.1
    # min_roll_value = -0.1
    radius = 50
    new_roll_value = NumericProperty()
    new_pitch_value = NumericProperty()

    def set_initial_values(self, heading, rolling, pitching):
        self.initial_rolling_value = rolling
        self.initial_pitching_value = pitching

    def set_roll_pos(self, rolling):
        self.new_roll_value = (rolling - self.initial_rolling_value) * (
                self.radius / (self.max_roll_value - self.min_roll_value))

    def set_pitch_pos(self, pitching):
        self.new_pitch_value = (pitching - self.initial_pitching_value) * (
                self.radius / (self.max_pitch_value - self.min_pitch_value))


class ProximityWidget(Widget):
    dr_value = 0
    color = ListProperty((1, 0.65, 0, 1))
    max_value = 800
    min_value = 0

    rectangle_count = 20
    rectangle_height = 300 / rectangle_count

    @staticmethod
    def set_dr_value(dr_value):
        ProximityWidget.dr_value = dr_value

    def set_proximity(self, value):
        diff = (value - ProximityWidget.dr_value) / 50
        direction = 1 if diff > 0 else -1
        self.canvas.clear()

        for i in range(min(abs(diff), ProximityWidget.rectangle_count / 2)):
            with self.canvas:
                Color(0.1 * i, 1 - 0.1 * i, 0, 0.5)

                Rectangle(
                    pos=(
                        self.center_x - self.width / 2 + 2,
                        self.center_y + direction * (i + abs((direction - 1) / 2)) * ProximityWidget.rectangle_height
                    ),
                    size=(self.width - 4, ProximityWidget.rectangle_height - 2)
                )


class PressureSensorWidget(Widget):
    max_dr_value = 1
    max_dr_radius_size = 50
    dr_circle_color = 0, 0, 0, 1
    patient_circle_color = 1, 0, 0, 1
    mean_circle_color = 1, 1, 1, 1

    dr_radius = NumericProperty()
    patient_radius = NumericProperty()
    mean_radius = NumericProperty()
    pressure = StringProperty()

    def __init__(self, **kwargs):
        super(PressureSensorWidget, self).__init__(**kwargs)
        self.mean_counter = 0
        self.mean_radius = 0

    def set_dr_radius(self, dr_value):
        self.dr_radius = float(dr_value) / PressureSensorWidget.max_dr_value * PressureSensorWidget.max_dr_radius_size

    def set_pressure(self, pressure):
        self.pressure = "{:.2f}".format(pressure)

        if pressure < 0:
            self.patient_radius = min(
                abs(float(pressure) / PressureSensorWidget.max_dr_value * PressureSensorWidget.max_dr_radius_size),
                1.5 * PressureSensorWidget.max_dr_radius_size,
            )
        else:
            self.patient_radius = 0
        self.set_mean()

    @staticmethod
    def set_max_dr_value(value):
        PressureSensorWidget.max_dr_value = value

    def set_mean(self):
        if self.patient_radius == 0:
            return

        mean_radius = self.mean_radius * self.mean_counter + self.patient_radius
        self.mean_counter += 1
        self.mean_radius = mean_radius / self.mean_counter


class SmartApp(App):
    def build(self):
        s = SmartWalker()
        Clock.schedule_interval(s.update, 0.1)
        Clock.schedule_interval(s.update_safe, 1.0)
        return s


if __name__ == '__main__':
    SmartApp().run()
