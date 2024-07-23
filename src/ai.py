import random
from settings import HEIGHT

class AI:
    def __init__(self, paddle, difficulty='medium'):
        self.paddle = paddle
        self.difficulty = difficulty
        self.speed = self.set_difficulty_speed(difficulty)

    def set_difficulty_speed(self, difficulty):
        if difficulty == 'easy':
            return 3
        elif difficulty == 'medium':
            return 5
        elif difficulty == 'hard':
            return 7
        else:
            return 5

    def move(self, ball):
        if self.difficulty == 'easy' and random.random() < 0.2:  # AI will miss the ball 20% of the time
            return
        elif self.difficulty == 'hard' and random.random() < 0.1:  # AI will miss the ball 10% of the time
            return

        if self.paddle.y + self.paddle.height // 2 < ball.y:
            self.paddle.y += self.speed
        elif self.paddle.y + self.paddle.height // 2 > ball.y:
            self.paddle.y -= self.speed

        # Ensure the paddle stays within screen bounds
        self.paddle.y = max(0, min(HEIGHT - self.paddle.height, self.paddle.y))
