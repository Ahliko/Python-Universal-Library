import time
import serial
from pypot.dynamixel import Dxl320IO, get_available_ports
import sys

serial_port = get_available_ports()[0]

ser = serial.Serial(serial_port, 1000000)
if not ser.isOpen():
    ser.open()

print(serial_port)


# Factory Reset
def factory_reset():
    print("Factory reset, you must see the motor LED flickering 4 times")
    print("Using protocol 2...")
    with Dxl320IO(serial_port, baudrate=1000000, timeout=0.1) as xl:
        xl.factory_reset(ids=list(range(253)))
    print("Done!")


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


# A simple example
def ex1():
    print("Starting a sin wave")
    with Dxl320IO(serial_port, baudrate=1000000, timeout=0.1) as xl:
        for i in motors:
            xl.set_moving_speed({i: 200.0})
            xl.enable_torque([i])
            xl.set_angle_limit({i: (0, 360)})
