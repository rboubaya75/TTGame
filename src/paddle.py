import pygame
from settings import HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT

class Paddle:
    def __init__(self, x, y, speed=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT

    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.y > 0:
            self.y -= self.speed
        if keys[down_key] and self.y < HEIGHT - self.height:
            self.y += self.speed

    def draw(self, screen, image):
        paddle_rect = image.get_rect(topleft=(self.x, self.y))
        screen.blit(image, paddle_rect)
