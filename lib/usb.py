"""Provides utility functions for directly interfacing with the robot base via a serial protocol.

See the documentation of the write() function for protocol spec.
"""

import logging

import serial.tools.list_ports
from serial import Serial


def connect() -> Serial:
    """Initialize the serial connection to an interactively chosen port."""
    ports = serial.tools.list_ports.comports()
    for i, port in enumerate(sorted(ports)):
        # "print" statements are required here for user input
        print(f"{i + 1}. {port.device}: {port.description} [{port.hwid}]")  # noqa: T201
    selected = ports[int(input("Port Number: ")) - 1].device

    conn = Serial(selected, 115200, timeout=1)
    conn.reset_input_buffer()

    if conn.is_open:
        logging.info("USB is working")
    else:
        logging.error("Failed to open port")

    return conn


def write(conn: Serial, message: str) -> None:
    """Send data via the serial connection.

    Available commands
    - INIT
    - MOVE <speed> <direction> <turn_speed>
    """
    logging.info("Executing command: %s", message)
    conn.write(message.encode())
