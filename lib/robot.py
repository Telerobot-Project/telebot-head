"""Abstraction over the USB connection to directly control robot movement."""

from typing import NamedTuple

from serial import Serial

from lib import usb


class RobotMovement(NamedTuple):
    """Movement instruction for the robot."""

    speed: int = 0
    direction: int = 0
    turn_speed: int = 0


def move_robot(connection: Serial, speed: int, direction: int, turn_speed: int) -> None:
    """Move the robot based on the current values of instance variables."""
    command = f"MOVE {speed:02} {direction:03} {turn_speed:03}\n"
    usb.write(connection, command)
