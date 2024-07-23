# tests/test_ball.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from ball import Ball
from paddle import Paddle
from settings import WIDTH, HEIGHT

class TestBall(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)

    def test_move(self):
        initial_x = self.ball.x
        initial_y = self.ball.y
        self.ball.move()
        self.assertNotEqual(initial_x, self.ball.x)
        self.assertNotEqual(initial_y, self.ball.y)

    def test_collision_with_walls(self):
        self.ball.x = WIDTH - self.ball.radius
        self.ball.vel_x = 5
        self.ball.check_collision(WIDTH, HEIGHT, Paddle(0, 0), Paddle(0, 0))
        self.assertEqual(self.ball.vel_x, -5)

if __name__ == "__main__":
    unittest.main()
