# net.py

import pygame
from settings import WHITE

class Net:
    def __init__(self, x, color=WHITE):
        self.x = x
        self.color = color
        self.segment_height = 20
        self.segment_gap = 10

    def draw(self, screen):
        for y in range(0, pygame.display.get_surface().get_height(), self.segment_height + self.segment_gap):
            pygame.draw.rect(screen, self.color, (self.x - 1, y, 2, self.segment_height))
