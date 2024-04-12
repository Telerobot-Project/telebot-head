from lib.usb_control import USB
import threading
from time import sleep

class Robot:
    def __init__(self):
        self.speed = 0
        self.max_speed = 60
        self.turn_speed = 0
        self.direction = 0

        self.usb = USB()
        self.connected = False

        self.raw_data = []
        self.gyro = 0
        self.us = [100] * 6
    
    def start(self):
        thread = threading.Thread(target=self.start_connection)
        thread.start()
    
    def start_connection(self):
        self.connected = False
        self.usb.start()
        self.usb.write('INIT\n')
        self.connected = True

        while self.connected:
            self.raw_data = self.usb.read()
            self.move()
            sleep(0.05)
    
    def close(self):
        self.connected = False
        self.usb.serial.close()

    def read(self):
        raw_data = self.usb.read()
    
    def move(self):
        speed = int(self.speed)
        direction = int(self.direction)
        turn_speed = int(self.turn_speed)
        command = 'MOVE '
        command += '0' * (2 - len(str(speed)))
        command += str(speed)
        command += ' '
        command += '0' * (3 - len(str(direction)))
        command += str(direction)
        command += ' '
        command += '0' * (3 - len(str(turn_speed)))
        command += str(turn_speed)
        command += '\n'
        print(command)
        self.usb.write(command)