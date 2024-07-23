import pygame
from settings import WIDTH, HEIGHT, FPS, WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, BALL_SIZE
from paddle import Paddle
from ball import Ball
from ai import AI

class Game:
    def __init__(self, screen, clock, ai_difficulty='medium', multiplayer=False):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.paused = False

        # Load and scale images
        self.table_image = pygame.image.load('assets/images/table.png')
        self.table_image = pygame.transform.scale(self.table_image, (WIDTH, HEIGHT))

        self.paddle_image = pygame.image.load('assets/images/paddle.jpg')
        self.paddle_image = pygame.transform.scale(self.paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

        self.ball_image = pygame.image.load('assets/images/ball.jpg')
        self.ball_image = pygame.transform.scale(self.ball_image, (BALL_SIZE, BALL_SIZE))

        self.ball = Ball(WIDTH // 2, HEIGHT // 2)
        self.paddle_left = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.paddle_right = Paddle(WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ai = AI(self.paddle_right, difficulty=ai_difficulty) if not multiplayer else None
        self.multiplayer = multiplayer
        self.player1_score = 0
        self.player2_score = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.serve_count = 0
        self.server = 1

    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.paddle_left, self.paddle_right)
        self.paddle_left.move(pygame.K_w, pygame.K_s)
        if self.multiplayer:
            self.paddle_right.move(pygame.K_UP, pygame.K_DOWN)
        else:
            self.ai.move(self.ball)

        if self.ball.x - self.ball.radius <= 0:  # Player 2 scores
            self.player2_score += 1
            self.serve_count += 1
            self.check_set_winner()
            self.reset_ball()
        elif self.ball.x + self.ball.radius >= WIDTH:  # Player 1 scores
            self.player1_score += 1
            self.serve_count += 1
            self.check_set_winner()
            self.reset_ball()

    def check_set_winner(self):
        if self.player1_score >= 11 and self.player1_score - self.player2_score >= 2:
            self.player1_sets += 1
            self.reset_scores()
        elif self.player2_score >= 11 and self.player2_score - self.player1_score >= 2:
            self.player2_sets += 1
            self.reset_scores()

    def reset_scores(self):
        self.player1_score = 0
        self.player2_score = 0

    def reset_ball(self):
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)

    def draw(self):
        self.screen.blit(self.table_image, (0, 0))
        self.paddle_left.draw(self.screen, self.paddle_image)
        self.paddle_right.draw(self.screen, self.paddle_image)
        self.ball.draw(self.screen, self.ball_image)
        self.draw_scores()
        pygame.display.flip()

    def draw_scores(self):
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.player1_score), True, WHITE)
        self.screen.blit(text, (250, 10))
        text = font.render(str(self.player2_score), True, WHITE)
        self.screen.blit(text, (WIDTH - 250, 10))
        text = font.render(f'Sets: {self.player1_sets}', True, WHITE)
        self.screen.blit(text, (50, 10))
        text = font.render(f'Sets: {self.player2_sets}', True, WHITE)
        self.screen.blit(text, (WIDTH - 150, 10))
