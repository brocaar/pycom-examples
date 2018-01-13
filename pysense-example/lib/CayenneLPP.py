"""
Source: https://github.com/simonqbs/cayennelpp-python
"""

import struct
import math

LPP_DIGITAL_INPUT = 0         # 1 byte
LPP_DIGITAL_OUTPUT = 1        # 1 byte
LPP_ANALOG_INPUT = 2          # 2 bytes, 0.01 signed
LPP_ANALOG_OUTPUT = 3         # 2 bytes, 0.01 signed
LPP_LUMINOSITY = 101          # 2 bytes, 1 lux unsigned
LPP_PRESENCE = 102            # 1 byte, 1
LPP_TEMPERATURE = 103         # 2 bytes, 0.1°C signed
LPP_RELATIVE_HUMIDITY = 104   # 1 byte, 0.5% unsigned
LPP_ACCELEROMETER = 113       # 2 bytes per axis, 0.001G
LPP_BAROMETRIC_PRESSURE = 115 # 2 bytes 0.1 hPa Unsigned
LPP_GYROMETER = 134           # 2 bytes per axis, 0.01 °/s
LPP_GPS = 136                 # 3 byte lon/lat 0.0001 °, 3 bytes alt 0.01 meter

# Data ID + Data Type + Data Size
LPP_DIGITAL_INPUT_SIZE = 3       # 1 byte
LPP_DIGITAL_OUTPUT_SIZE = 3      # 1 byte
LPP_ANALOG_INPUT_SIZE = 4        # 2 bytes, 0.01 signed
LPP_ANALOG_OUTPUT_SIZE = 4       # 2 bytes, 0.01 signed
LPP_LUMINOSITY_SIZE = 4          # 2 bytes, 1 lux unsigned
LPP_PRESENCE_SIZE = 3            # 1 byte, 1
LPP_TEMPERATURE_SIZE = 4         # 2 bytes, 0.1°C signed
LPP_RELATIVE_HUMIDITY_SIZE = 3   # 1 byte, 0.5% unsigned
LPP_ACCELEROMETER_SIZE = 8       # 2 bytes per axis, 0.001G
LPP_BAROMETRIC_PRESSURE_SIZE = 4 # 2 bytes 0.1 hPa Unsigned
LPP_GYROMETER_SIZE = 8           # 2 bytes per axis, 0.01 °/s
LPP_GPS_SIZE = 11                # 3 byte lon/lat 0.0001 °, 3 bytes alt 0.01 meter

class CayenneLPP:
    def __init__(self):
        self.buffer = bytearray()

    def get_buffer(self):
        return self.buffer

    def reset(self):
        self.buffer = bytearray()

    def get_size(self):
        return len(self.buffer)

    def add_temperature(self, channel, value):
        val = math.floor(value * 10);

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_TEMPERATURE))
        self.buffer.extend(struct.pack('b', val >> 8))
        self.buffer.extend(struct.pack('b', val))

    def add_relative_humidity(self, channel, value):
        val = math.floor(value * 2)

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_RELATIVE_HUMIDITY))
        self.buffer.extend(struct.pack('b', val))

    def add_digital_input(self, channel, value):
        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_DIGITAL_INPUT))
        self.buffer.extend(struct.pack('b', value))

    def add_digital_output(self, channel, value):
        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_DIGITAL_OUTPUT))
        self.buffer.extend(struct.pack('b', value))

    def add_analog_input(self, channel, value):
        val = math.floor(value * 100)

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_ANALOG_INPUT))
        self.buffer.extend(struct.pack('b', val >> 8))
        self.buffer.extend(struct.pack('b', val))

    def add_analog_output(self, channel, value):
        val = math.floor(value * 100)

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_ANALOG_OUTPUT))
        self.buffer.extend(struct.pack('b', val >> 8))
        self.buffer.extend(struct.pack('b', val))

    def add_luminosity(self, channel, value):
        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_LUMINOSITY))
        self.buffer.extend(struct.pack('b', value >> 8))
        self.buffer.extend(struct.pack('b', value))

    def add_presence(self, channel, value):
        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_PRESENCE))
        self.buffer.extend(struct.pack('b', value))

    def add_accelerometer(self, channel, x, y, z):
        vx = math.floor(x * 1000)
        vy = math.floor(y * 1000)
        vz = math.floor(z * 1000)

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_ACCELEROMETER))        
        self.buffer.extend(struct.pack('b', vx >> 8))
        self.buffer.extend(struct.pack('b', vx))
        self.buffer.extend(struct.pack('b', vy >> 8))
        self.buffer.extend(struct.pack('b', vy))        
        self.buffer.extend(struct.pack('b', vz >> 8))
        self.buffer.extend(struct.pack('b', vz))        

    def add_barometric_pressure(self, channel, value):
        val = math.floor(value * 10)

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_BAROMETRIC_PRESSURE))
        self.buffer.extend(struct.pack('b', val >> 8))
        self.buffer.extend(struct.pack('b', val))                

    def add_gryrometer(self, channel, x, y, z):
        vx = math.floor(x * 100)
        vy = math.floor(y * 100)
        vz = math.floor(z * 100)

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_GYROMETER))        
        self.buffer.extend(struct.pack('b', vx >> 8))
        self.buffer.extend(struct.pack('b', vx))
        self.buffer.extend(struct.pack('b', vy >> 8))
        self.buffer.extend(struct.pack('b', vy))        
        self.buffer.extend(struct.pack('b', vz >> 8))
        self.buffer.extend(struct.pack('b', vz))

    def add_gps(self, channel, latitude, longitude, meters):
        lat = math.floor(latitude * 10000)
        lon = math.floor(longitude * 10000)
        alt = math.floor(meters * 100)

        self.buffer.extend(struct.pack('b', channel))
        self.buffer.extend(struct.pack('b', LPP_GPS))
        self.buffer.extend(struct.pack('b', lat >> 16))
        self.buffer.extend(struct.pack('b', lat >> 8))
        self.buffer.extend(struct.pack('b', lat))
        self.buffer.extend(struct.pack('b', lon >> 16))
        self.buffer.extend(struct.pack('b', lon >> 8))
        self.buffer.extend(struct.pack('b', lon))        
        self.buffer.extend(struct.pack('b', alt >> 16))
        self.buffer.extend(struct.pack('b', alt >> 8))
        self.buffer.extend(struct.pack('b', alt))