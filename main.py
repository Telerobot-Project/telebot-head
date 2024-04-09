from lib.video import Video
from lib.ui import Window
from lib.server import Server
from lib.robot import Robot

window = Window(450, 700, "TeleBOT")
robot = Robot()
user_video = Video(window)
usb_video = Video(window, (1280, 720))
tof_video = Video(window)
server = Server(user_video, usb_video, tof_video, robot)

server.start()
window.start()
usb_video.start()

while True:
    window.read()
    if not window.run:
        break
    usb_video.read()

    window.fill((34, 34, 34))
    user_video.draw(0, 0, 450, 700)
    usb_video.draw(359, 564, 81, 126)
    window.draw_text(
        f'{robot.speed}, {robot.direction}, {robot.turn_speed}', 0, 678, (255, 255, 255))
    window.update()

print('Closing')
server.close()
usb_video.close()
