import pypot.dynamixel as dynamixel
import sys
import time
import serial
import math
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pypot.dynamixel.conversion import dynamixelModels
from pypot.dynamixel import DxlIO, Dxl320IO, get_available_ports
from pypot.utils import flushed_print as print
import sys

sys.path.append("/webcam.py")

ser = serial.Serial("COM4", 1000000)
if not ser.isOpen():
    ser.open()
serial_port = "COM4"
print(serial_port)
# # Factory Reset
# print("Factory reset, you must see the motor LED flickering 4 times")
# print("Using protocol 2...")
# with Dxl320IO(serial_port, baudrate=1000000, timeout=0.1) as io:
#     io.factory_reset(ids=list(range(253)))
# print("Done!")

motors = []
# Wait for the motor to "reboot..."
for _ in range(10):
    with Dxl320IO(serial_port, baudrate=1000000) as io:
        time.sleep(1)
        motors = (io.scan(range(20)))
        if io.ping(1):
            break

else:
    print("Could not communicate with the motor...")
    print("Make sure one (and only one) is connected and try again")
    print("If the issue persists, use Dynamixel wizard to attempt a firmware recovery")
    sys.exit(1)

print("Success!")
print("Found motor(s): {}".format(motors))


def coucou(id, pos):
    with Dxl320IO(serial_port, baudrate=1000000, timeout=0.1) as io:
        io.set_goal_position({id: pos})


print("Starting a sin wave")
with Dxl320IO(serial_port, baudrate=1000000, timeout=0.1) as io:
    for i in motors:
        io.set_moving_speed({i: 200.0})
        io.enable_torque([i])
        io.set_angle_limit({i: (0, 360)})