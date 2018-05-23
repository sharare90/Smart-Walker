from Dependencies.HX711 import HX711

class WeightSensor(HX711):

    def __init__(self, dout, pd_sck):
        super(WeightSensor, self).__init__(dout, pd_sck)

    # sets the endianness of the sensor, and calibrates it
    # TODO: set_reference_unit parameter is currently a throwaway value
    # it needs to be determined experimentally
    def initialize_weight_sensor(self):
        self.set_reading_format("LSB", "MSB")
        self.set_reference_unit(92)
        self.reset()
        self.tare()
        