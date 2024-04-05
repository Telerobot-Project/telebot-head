from lib.video import Video
from lib.ui import Window
from lib.server import Server

window = Window(450, 700, "TeleBOT")
user_video = Video(window)
usb_video = Video(window)
tof_video = Video(window)
server = Server(user_video, usb_video, tof_video)

server.start()
window.start()
usb_video.start()

while True:
    window.read()
    if not window.run: break
    usb_video.read()

    if server.connected:
        server.sendall()

    window.fill((34, 34, 34))
    user_video.draw(0, 0, 450, 700)
    usb_video.draw(359, 564, 81, 126)
    window.update()

print('Closing')
server.close()
usb_video.close()