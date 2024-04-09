import cv2
import numpy
import pygame
import pickle
import imutils
from numpy import rot90

class Video:
    def __init__(self, window, size = None):
        self.frame = None
        self.surface = None
        self.binary = None
        self.window = window
        self.new_data = False
        self.size = size

    def start(self, i=0):
        self.obj = cv2.VideoCapture(i)
        if self.size is not None:
            self.obj.set(cv2.CAP_PROP_FRAME_WIDTH, self.size[0])
            self.obj.set(cv2.CAP_PROP_FRAME_HEIGHT, self.size[1])
        self.width = int(self.obj.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.obj.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def read(self):
        if self.obj.isOpened():
            _, self.frame = self.obj.read()
            self.frame = rot90(self.frame)
            if self.frame is not None:
                self.new_data = True
        return self.frame

    def draw(self, x, y, width, height):
        if self.frame is None:
            pygame.draw.rect(self.window.screen, (0, 0, 0),
                             (x, y, width, height))
        else:
            self.surface = self.frame

            if width / self.width > height / self.height:
                self.surface = imutils.resize(self.surface, width=width)
                new_height = self.height * (width / self.width)
                crop = (new_height - height) / 2
                self.surface = self.surface[int(crop): int(
                    new_height - crop), 0: width]
            else:
                self.surface = imutils.resize(self.surface, height=height)
                new_width = self.width * (height / self.height)
                crop = (new_width - width) / 2
                self.surface = self.surface[0: height, int(
                    crop): int(new_width - crop)]

            self.surface = cv2.cvtColor(self.surface, cv2.COLOR_BGR2RGB)
            self.surface = numpy.rot90(self.surface)
            self.surface = pygame.surfarray.make_surface(self.surface)
            self.window.screen.blit(self.surface, (x, y))
            pygame.draw.rect(self.window.screen, (0, 0, 0),
                             (x, y, width, height), 1)

    def get_binary(self, width=320):
        self.binary = self.frame
        self.binary = imutils.resize(self.binary, width=width)
        self.binary = pickle.dumps(self.binary)
        return self.binary

    def unpack(self):
        buf = pickle.loads(self.binary)
        self.width = buf.shape[1]
        self.height = buf.shape[0]
        self.frame = buf
        return self.frame

    def close(self):
        self.obj.release()
