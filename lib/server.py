"""A socket client for communicating with the client via a binary protocol.

Packets received from the client have the following structure:
    int        : robot movement speed
    int        : robot direction
    int        : robot rotation speed
    ulong long : size of the video data
    ...        : video data

Packets sent to the client have the following structure:
    int        : gyroscope measurement
    int[6]     : ultrasonic sensor measurements
    ulong long : size of the video data
    ...        : video data

"""

import logging
import socket
import struct
import threading
from struct import calcsize
from typing import NamedTuple

from lib import usb

from .robot import RobotMovement, move_robot
from .video import CameraVideo, Video


class ConnectionInfo(NamedTuple):
    """IP address and port of the robot."""

    host: str = "localhost"
    port: int = 5050


class RobotVideo(NamedTuple):
    """A bundle of camera video and ToF video from the robot."""

    camera: CameraVideo
    tof: CameraVideo


class Server:
    """A socket server for communicating with the client via a binary protocol."""

    def __init__(
        self,
        user_video: Video,
        robot_video: RobotVideo,
        host: ConnectionInfo,
    ) -> None:
        """Initialize the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run = True

        self.user_video = user_video
        self.robot_video = robot_video

        self.robot = usb.connect()
        usb.write(self.robot, "INIT\n")
        self.movement = RobotMovement()

        self.data = b""

        self.socket.bind(host)
        self.socket.listen()
        logging.info("Connecting to the client...")
        self.conn, _ = self.socket.accept()
        logging.info("Client connected")

        threading.Thread(target=self.__read_loop).start()
        threading.Thread(target=self.__send_loop).start()

    def __read_loop(self) -> None:
        """Loop that receives data from the client."""
        while self.run:
            try:
                self.__receive_movement()
                self.__receive_video()

                self.user_video.unpack()
            except Exception:
                logging.exception("Error while running the read loop")

    def __receive_movement(self) -> None:
        """Receive robot movement instructions and move the robot."""
        data_size = calcsize("iii")

        while len(self.data) < data_size:
            self.data += self.conn.recv(4 * 1024)

        movement_instruction = struct.unpack(
            "iii",
            self.data[:data_size],
        )
        move_robot(self.robot, *movement_instruction)
        self.movement = RobotMovement(*movement_instruction)

        self.data = self.data[data_size:]

    def __receive_video(self) -> None:
        """Receive user camera video."""
        header_size = struct.calcsize("Q")

        while len(self.data) < header_size:
            self.data += self.conn.recv(4 * 1024)

        video_size = struct.unpack("Q", self.data[:header_size])[0]
        self.data = self.data[header_size:]

        while len(self.data) < video_size:
            self.data += self.conn.recv(4 * 1024)

        self.user_video.binary = self.data[:video_size]
        self.data = self.data[video_size:]

    def __send_loop(self) -> None:
        """Loop that sends data to the client."""
        while self.run:
            try:
                if self.robot_video.camera.new_data:
                    self.__send_data()
                    self.robot_video.camera.new_data = False
            except Exception:
                logging.exception("Error while running the send loop")

    def __send_data(self) -> None:
        """Send robot state and video data to the client."""
        self.robot_video.camera.pack()

        self.send_buffer = b""
        self.send_buffer += struct.pack(
            "iiiiiii",
            0,
            *([100] * 6),
        )
        self.send_buffer += struct.pack("Q", len(self.robot_video.camera.binary))
        self.send_buffer += self.robot_video.camera.binary
        self.conn.sendall(self.send_buffer)

    def close(self) -> None:
        """Close the socket connection."""
        self.run = False
        self.robot.close()
        self.socket.close()
