from lib.video import Video
from lib.ui import Window
from lib.server import Server
from lib.robot import Robot
from lib.tof_camera import ToFCamera

window = Window(600, 1024, "TeleBOT")
robot = Robot()
user_video = Video(window)
usb_video = Video(window, (1280, 720))
tof_video = Video(window)
tof_camera = ToFCamera(tof_video)
server = Server(user_video, usb_video, tof_video, robot, host='192.168.8.101', port=5050)

server.start()
window.start()
usb_video.start()
robot.start()

while True:
    window.read()
    if not window.run:
        break
    usb_video.read()
    # tof_video.read()

    window.fill((34, 34, 34))
    user_video.draw(0, 0, 600, 1024)
    usb_video.draw(482, 822, 108, 192)
    window.draw_text(
        f'{robot.speed}, {robot.direction}, {robot.turn_speed}', 0, 1001, (255, 255, 255))
    window.update()

print('Closing')
server.close()
usb_video.close()
