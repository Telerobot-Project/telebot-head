"""Provides a class for storing and managing video data."""

import pickle

import cv2
import imutils  # type: ignore[import-untyped]
import numpy as np
import pygame
from cv2 import UMat

from .ui import Rectangle, Window


class Video:
    """Class for storing video data."""

    def __init__(self, window: Window) -> None:
        """Initialize a new video."""
        self.frame: UMat | None = None
        self.binary = b""
        self.window = window
        self.new_data = False

    def draw(self, rect: Rectangle) -> None:
        """Draw the video on the screen."""
        if self.frame is None:
            pygame.draw.rect(self.window.screen, (0, 0, 0), rect)
        else:
            surface_data = self.frame.get()

            if rect.width / self.width > rect.height / self.height:
                surface_data = imutils.resize(surface_data, width=rect.width)
                new_height = self.height * (rect.width / self.width)
                crop = (new_height - rect.height) / 2
                surface_data = surface_data[
                    int(crop) : int(new_height - crop),
                    0 : rect.width,
                ]
            else:
                surface_data = imutils.resize(surface_data, height=rect.height)
                new_width = self.width * (rect.height / self.height)
                crop = (new_width - rect.width) / 2
                surface_data = surface_data[
                    0 : rect.height,
                    int(crop) : int(new_width - crop),
                ]

            surface_data = cv2.cvtColor(surface_data, cv2.COLOR_BGR2RGB)
            surface_data = np.rot90(surface_data)
            surface = pygame.surfarray.make_surface(surface_data)

            surface = pygame.transform.rotate(surface, 90)
            rect = Rectangle(
                x=rect.y,
                y=rect.x,
                width=rect.height,
                height=rect.width,
            )

            self.window.screen.blit(surface, (rect.x, rect.y))
            pygame.draw.rect(self.window.screen, (0, 0, 0), rect, 1)

    def pack(self, width: int = 200) -> None:
        """Convert the video frame to binary data."""
        if self.frame is not None:
            frame_data = self.frame.get()
            self.binary = imutils.resize(frame_data, width=width)
            self.binary = pickle.dumps(self.binary)

    def unpack(self) -> None:
        """Get the video frame from binary data."""
        buf = pickle.loads(self.binary)
        self.width = buf.shape[1]
        self.height = buf.shape[0]
        self.frame = buf


class CameraVideo(Video):
    """Video data received from robot's camera."""

    def __init__(self, window: Window, size: tuple[int, int] | None = None) -> None:
        """Initialize a new video."""
        super().__init__(window)

        self.obj = cv2.VideoCapture(0)
        if size is not None:
            self.obj.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
            self.obj.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
            self.width = size[1]
            self.height = size[0]
        else:
            self.width = int(self.obj.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.height = int(self.obj.get(cv2.CAP_PROP_FRAME_WIDTH))

    def read(self) -> None:
        """Read a video frame from the camera."""
        if self.obj.isOpened():
            _, frame_data = self.obj.read()
            frame_data = np.rot90(frame_data, -1)
            if frame_data is not None:
                self.frame = UMat(frame_data)  # type: ignore[call-overload]
                self.new_data = True

    def close(self) -> None:
        """Close the opencv video capture."""
        self.obj.release()
