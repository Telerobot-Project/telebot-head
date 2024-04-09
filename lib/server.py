import socket
import cv2
import pickle
import struct
from struct import calcsize
import imutils
import threading
from time import sleep
from lib.video import Video
from lib.robot import Robot


class Server:
    def __init__(self, user_video: Video, usb_video: Video, tof_video: Video, robot: Robot, host: str = None, port: int = 5050):
        if host is not None:
            self.host = host
        else:
            self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.addr = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.run = True

        self.user_video = user_video
        self.usb_video = usb_video
        self.tof_video = tof_video
        self.robot = robot

        self.data = b''
        self.payload_size = struct.calcsize("Q")

    def start(self):
        self.socket.bind(self.addr)
        self.socket.listen()

        self.start_thread = threading.Thread(target=self.start_connection)
        self.start_thread.start()

    def start_connection(self):
        self.connected = False
        print(f'LISTENING ON {self.host}:{self.port}')
        self.client_socket, self.addr = self.socket.accept()
        print(f'CONNECTED TO {self.addr}')
        self.connected = True

        self.read_thread = threading.Thread(target=self.read_loop)
        self.read_thread.start()

        self.send_thread = threading.Thread(target=self.send_loop)
        self.send_thread.start()

    def read_loop(self):
        while self.run:
            try:
                self.receive_data()
                self.receive_video(self.user_video)

                self.user_video.unpack()
            except:
                pass

    def send_loop(self):
        while self.run:
            try:
                if self.usb_video.new_data:
                    self.send_data()
                    self.usb_video.new_data = False
            except:
                pass

    def send_data(self):
        self.usb_video.get_binary()

        self.send_buffer = b''
        self.send_buffer += struct.pack("iiiiiii", self.robot.gyro,
                                        self.robot.us[0], self.robot.us[1], self.robot.us[2], self.robot.us[3], self.robot.us[4], self.robot.us[5])
        self.send_buffer += struct.pack("Q", len(self.usb_video.binary))
        self.send_buffer += self.usb_video.binary
        self.client_socket.sendall(self.send_buffer)

    def receive_data(self):
        while len(self.data) < calcsize("iii"):
            self.data += self.client_socket.recv(4*1024)

        self.robot.speed, self.robot.direction, self.robot.turn_speed = struct.unpack(
            "iii", self.data[:calcsize("iii")])
        self.data = self.data[calcsize("iii"):]

    def receive_video(self, video_obj: Video):
        while len(self.data) < self.payload_size:
            self.data += self.client_socket.recv(4*1024)

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.client_socket.recv(4*1024)

        video_obj.binary = self.data[:msg_size]
        self.data = self.data[msg_size:]

    def close(self):
        self.connected = False
        self.run = False
        self.socket.close()
