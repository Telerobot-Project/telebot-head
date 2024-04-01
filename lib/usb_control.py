from serial import Serial
import serial.tools.list_ports


class USB:
    def __init__(self) -> None:
        self.port = None
        self.serial = None

    def start(self):
        ports = serial.tools.list_ports.comports()
        for i, (port, desc, hwid) in enumerate(sorted(ports)):
            print("{}. {}: {} [{}]".format(i+1, port, desc, hwid))
        self.port, _, _ = ports[int(input('Port Number: ')) - 1]

        self.serial = Serial(self.port, 115200, timeout=1)
        self.serial.reset_input_buffer()

        if self.serial.is_open:
            print('USB is working')
        else:
            print('Failed to open port')

    def read(self):
        if self.serial.in_waiting > 0:
            data = self.serial.read_all().decode('utf-8').rstrip()
            print(data)

    def write(self):
        message = input('WRITE -> ')
        self.serial.write(message.encode())


if __name__ == '__main__':
    print('Read - 0')
    print('Write - 1')
    mode = int(input('Mode (0/1): ').strip())
    usb = USB()
    usb.start()
    try:
        while True:
            if mode:
                usb.write()
            else:
                usb.read()
    except KeyboardInterrupt:
        usb.serial.close()
        print('\nUSB is closed')
