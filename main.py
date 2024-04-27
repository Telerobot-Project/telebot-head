"""On-screen robot UI and server for communicating with the client."""

from lib.server import ConnectionInfo, RobotVideo, Server
from lib.tof_camera import ToFCamera
from lib.ui import Point, Rectangle, Window
from lib.video import CameraVideo, Video

window = Window(536, 1024, "TeleBOT")
user_video = Video(window)
usb_video = CameraVideo(window, (1280, 720))
tof_video = CameraVideo(window)
tof_camera = ToFCamera(tof_video)
server = Server(
    user_video,
    RobotVideo(usb_video, tof_video),
    ConnectionInfo("192.168.8.101", 5050),
)

while True:
    window.read()
    if not window.run:
        break

    usb_video.read()
    # TODO read ToF camera

    window.fill((34, 34, 34))
    user_video.draw(Rectangle(x=0, y=0, width=536, height=1024))
    usb_video.draw(Rectangle(x=418, y=822, width=108, height=192))
    window.draw_text(
        f"{server.movement.speed}, {server.movement.direction}, {server.movement.turn_speed}",
        Point(0, 1001),
        (255, 255, 255),
    )
    window.update()

server.close()
usb_video.close()
