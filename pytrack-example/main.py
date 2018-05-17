import socket
import time
import binascii
import pycom
from network import LoRa

from CayenneLPP import CayenneLPP
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
from L76GNSS import L76GNSS


py = Pytrack()
li = LIS2HH12(py)

# after 60 seconds of waiting without a GPS fix it will
# return None, None
gnss = L76GNSS(py, timeout=120)


# Disable heartbeat LED
pycom.heartbeat(False)

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters
app_eui = binascii.unhexlify('0101010101010101')
app_key = binascii.unhexlify('11B0282A189B75B0B4D2D8C7FA38548B')

print("DevEUI: %s" % (binascii.hexlify(lora.mac())))
print("AppEUI: %s" % (binascii.hexlify(app_eui)))
print("AppKey: %s" % (binascii.hexlify(app_key)))

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(0x140000)
    time.sleep(2.5)
    pycom.rgbled(0x000000)
    time.sleep(1.0)
    print('Not yet joined...')

print('OTAA joined')
pycom.rgbled(0x001400)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

while True:
    s.setblocking(True)
    pycom.rgbled(0x000014)
    lpp = CayenneLPP()

    print('\n\n** 3-Axis Accelerometer (LIS2HH12)')
    print('Acceleration', li.acceleration())
    print('Roll', li.roll())
    print('Pitch', li.pitch())
    lpp.add_accelerometer(1, li.acceleration()[0], li.acceleration()[1], li.acceleration()[2])
    lpp.add_gryrometer(1, li.roll(), li.pitch(), 0)

    print('\n\n** GPS (L76GNSS)')
    loc = gnss.coordinates()
    if loc[0] == None or loc[1] == None:
        print('No GPS fix within configured timeout :-(')
    else:
        print('Latitude', loc[0])
        print('Longitude', loc[1])
        lpp.add_gps(1, loc[0], loc[1], 0)

    print('Sending data (uplink)...')
    s.send(bytes(lpp.get_buffer()))
    s.setblocking(False)
    data = s.recv(64)
    print('Received data (downlink)', data)
    pycom.rgbled(0x001400)
    time.sleep(30)
