import pygame
import math

class Window:
    def __init__(self, width, height, caption):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.caption = caption
        self.run = True

    def start(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.SysFont('Arial', 15)
        self.clock = pygame.time.Clock()
    
    def read(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

    def update(self):
        self.clock.tick(25)
        pygame.display.update()

    def close(self):
        pygame.quit()
        self.run = False

    def fill(self, color):
        self.screen.fill(color)

    def draw_text(self, text, x, y, color):
        self.screen.blit(self.font.render(text, True, color), (x, y))

    def draw_multi_line(self, lines, x, y):
        for i, l in enumerate(lines):
            self.draw_text(l, x, y + 20*i, (255, 255, 255))

    def draw_video(self, image, x, y):
        self.screen.blit(image, (x, y))
