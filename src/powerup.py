# powerup.py

import pygame
import random
from settings import WHITE

class PowerUp:
    def __init__(self, width, height):
        self.x = random.randint(50, width - 50)
        self.y = random.randint(50, height - 50)
        self.size = 20
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def apply_effect(self, paddle):
        paddle.height += 50
