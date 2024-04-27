"""Rendering of the on-screen UI."""

from typing import NamedTuple

import pygame

Color = tuple[int, int, int]


class Point(NamedTuple):
    """A point on the screen with x and y coordinates."""

    x: int
    y: int


class Rectangle(NamedTuple):
    """A rectangle/bounding box for a UI element."""

    x: int
    y: int
    width: int
    height: int


class Window:
    """The main application window."""

    def __init__(self, width: int, height: int, caption: str) -> None:
        """Initialize the window."""
        pygame.init()
        pygame.font.init()

        # The video is rotated by 90°
        self.screen = pygame.display.set_mode((height, width))

        pygame.display.set_caption(caption)
        self.font = pygame.font.SysFont("Arial", 15)
        self.clock = pygame.time.Clock()

        self.run = True

    def read(self) -> None:
        """Process quit events from the pygame queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()

    def update(self) -> None:
        """Refresh the contents of the pygame window."""
        self.clock.tick(30)
        pygame.display.update()

    def fill(self, color: Color) -> None:
        """Fill the window with a solid color."""
        self.screen.fill(color)

    def draw_text(self, text: str, position: Point, color: Color) -> None:
        """Draw text to the screen."""
        self.screen.blit(
            pygame.transform.rotate(
                self.font.render(
                    text,
                    antialias=True,
                    color=color,
                ),
                90,
            ),
            # Swap x and y because the frame is rotated by 90°
            position[::-1],
        )
