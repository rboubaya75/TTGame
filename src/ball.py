import pygame
from settings import BALL_SPEED, BALL_SIZE, WIDTH, HEIGHT

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = BALL_SPEED
        self.vy = BALL_SPEED
        self.radius = BALL_SIZE // 2

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.vy = -self.vy

    def check_collision(self, paddle_left, paddle_right):
        if self.x - self.radius <= paddle_left.x + paddle_left.width and self.y >= paddle_left.y and self.y <= paddle_left.y + paddle_left.height:
            self.vx = -self.vx
        if self.x + self.radius >= paddle_right.x and self.y >= paddle_right.y and self.y <= paddle_right.y + paddle_right.height:
            self.vx = -self.vx

    def draw(self, screen, image):
        ball_rect = image.get_rect(center=(self.x, self.y))
        screen.blit(image, ball_rect)
