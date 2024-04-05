import socket
import cv2
import pickle
import struct
from struct import calcsize
import imutils
import threading
from time import sleep
from lib.video import Video

class Server:
    def __init__(self, user_video: Video, usb_video: Video, tof_video: Video):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.addr = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.run = True

        self.user_video = user_video
        self.usb_video = usb_video
        self.tof_video = tof_video

        self.data = b''
        self.payload_size = struct.calcsize("Q")
    
    def start(self):
        self.socket.bind(self.addr)
        self.socket.listen()

        self.thread = threading.Thread(target=self.loop, args=())
        self.thread.start()
    
    def loop(self):
        while self.run:
            try:
                self.start_connection()
            except:
                pass
            
            self.run = False
            while self.connected:
                self.receive_video(self.user_video)
                self.user_video.unpack()

    def sendall(self):
        self.usb_video.get_binary()
        self.client_socket.sendall(struct.pack("Q", len(self.usb_video.binary)) + self.usb_video.binary)
    
    def start_connection(self):
        self.connected = False
        print(f'LISTENING ON {self.host}:{self.port}')
        self.client_socket, self.addr = self.socket.accept()
        print(f'CONNECTED TO {self.addr}')
        self.connected = True

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