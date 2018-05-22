from Dependencies.HX711 import HX711

class WeightSensor(HX711):

    def __init__(self, dout, pd_sck):
        super().__init__(dout, pd_sck)

    def initialize_weight_sensor(self):
        sensor.set_reading_format("LSB", "MSB")
        sensor.set_reference_unit(92)
        sensor.reset()
        sensor.tare()