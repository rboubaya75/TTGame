# tests/test_ai.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from ai import AI
from paddle import Paddle
from ball import Ball

class TestAI(unittest.TestCase):
    def setUp(self):
        self.paddle = Paddle(50, 50)
        self.ai = AI(self.paddle)

    def test_move(self):
        ball = Ball(50, 60)
        self.ai.move(ball)
        self.assertTrue(self.paddle.y > 50)

if __name__ == "__main__":
    unittest.main()
