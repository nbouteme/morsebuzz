import serial;
import time;

ser = serial.Serial('/dev/ttyACM0', timeout=1.0)

while True:
    ser.write(input());