# tests/test_paddle.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from paddle import Paddle

class TestPaddle(unittest.TestCase):
    def setUp(self):
        self.paddle = Paddle(50, 50)

    def test_move(self):
        initial_y = self.paddle.y
        self.paddle.vel = 5
        self.paddle.move()
        self.assertEqual(self.paddle.y, initial_y + 5)

if __name__ == "__main__":
    unittest.main()
