import pygame
import math
from lib.usb_control import USB

usb = USB()

pygame.init()
size = width, height = 640, 320
title = "Robot control"

window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption(title)

mouse_down = False
robot_speed, robot_direction = 0, 0
robot_max_speed = 60
robot_data, raw_data = [], []
robot_command = ''

circle_coord = [0, 0]
circle_dist = 0

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 15)

text = []

def render_multi_line(lines, x, y, fsize):
    for i, l in enumerate(lines):
        window.blit(my_font.render(l, 0, (255, 255, 255)), (x, y + fsize*i))

def draw_window():
    window.fill((0, 0, 0))
    pygame.draw.circle(window, (255, 255, 255), (160, 160), 100, 5)
    pygame.draw.circle(window, (255, 255, 255), (int(circle_coord[0] + 160), int(circle_coord[1] + 160)), 20)
    pygame.draw.line(window, (255, 255, 255), (320 - 2, 0), (320 - 2, 320), 4)
    render_multi_line(text, 335, 15, 20)
    pygame.display.flip()  

if __name__ == '__main__':
    usb.start()

    run = True
    while run:
        raw_data = usb.read()
        robot_data = raw_data if raw_data != None else robot_data
        text = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False;
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
        
        if mouse_down:
            circle_coord = list(pygame.mouse.get_pos())
            circle_coord = [circle_coord[0] - 160, circle_coord[1] - 160]
            circle_dist = math.sqrt(circle_coord[0] ** 2 + circle_coord[1] ** 2)
            if circle_dist >= 100:
                circle_coord[0] /= circle_dist / 100
                circle_coord[1] /= circle_dist / 100
                circle_dist = 100
        else:
            circle_coord = [0, 0]
            circle_dist = 0
        
        robot_speed = int(circle_dist / 100 * robot_max_speed)
        robot_direction = int(math.atan2(circle_coord[0], circle_coord[1] * -1) / math.pi * 180)
        robot_direction = (robot_direction + 360) % 360

        text.append(f'robot speed = {robot_speed}/{robot_max_speed}')
        text.append(f'robot direction = {robot_direction}')

        robot_command = 'MOVE '
        robot_command += '0' * (2 - len(str(robot_speed)))
        robot_command += str(robot_speed)
        robot_command += ' '
        robot_command += '0' * (3 - len(str(robot_direction)))
        robot_command += str(robot_direction)
        robot_command += '\n'
        # if mouse_down:
        usb.write(robot_command)
        print(f'WRITE: {robot_command[:-1]}')
            # mouse_down = 0

        # print(robot_data)

        draw_window()
        clock.tick(20)

    pygame.quit()
    usb.serial.close()
