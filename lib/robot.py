from lib.usb_control import USB

class Robot:
    def __init__(self):
        self.speed = 0
        self.max_speed = 60
        self.turn_speed = 0
        self.direction = 0

        self.usb = USB()

        self.raw_data = []
        self.gyro = 0
        self.us = [100] * 6
    
    def start(self):
        self.usb.start()
        self.usb.write('INIT\n')
    
    def close(self):
        self.usb.serial.close()

    def read(self):
        raw_data = self.usb.read()
    
    def move(self):
        command = 'MOVE '
        command += '0' * (2 - len(str(self.speed)))
        command += str(self.speed)
        command += ' '
        command += '0' * (3 - len(str(self.direction)))
        command += str(self.direction)
        command += '\n'
        self.usb.write(command)