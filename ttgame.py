import pygame
import random
import sys

# Settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TABLE_COLOR = (0, 128, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30
POWERUP_AREA_MARGIN = 50  # Margin from the edges of the screen

# Initialize Pygame and load sounds
pygame.mixer.init()
hit_sound = pygame.mixer.Sound('assets/sounds/paddle.wav')
score_sound = pygame.mixer.Sound('assets/sounds/score.wav')
powerup_sound = pygame.mixer.Sound('assets/sounds/powerup.wav')

# Paddle class
class Paddle:
    def __init__(self, x, y, image_path, width=50, height=100):
        self.x = x
        self.y = y
        self.original_width = width
        self.original_height = height
        self.width = width
        self.height = height
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.vel = 0
        self.powerup_effect = None

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        self.y += self.vel
        # Ensure the paddle stays within screen bounds
        if self.y - self.height // 2 < 0:
            self.y = self.height // 2
        elif self.y + self.height // 2 > HEIGHT:
            self.y = HEIGHT - self.height // 2
        self.rect.center = (self.x, self.y)

    def handle_event(self, event, player=1):
        if player == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.vel = -5
                elif event.key == pygame.K_DOWN:
                    self.vel = 5
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.vel = 0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.vel = -5
                elif event.key == pygame.K_s:
                    self.vel = 5
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    self.vel = 0

    def apply_powerup(self, effect):
        if effect == 'speed':
            self.vel *= 2
            self.powerup_effect = 'speed'
            print(f"Speed power-up applied: Velocity is now {self.vel}")
        elif effect == 'size':
            self.width = int(self.original_width * 2)
            self.height = int(self.original_height * 2)
            self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (self.width, self.height))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.powerup_effect = 'size'
            print("Size power-up applied")

    def reset_powerup(self):
        if self.powerup_effect == 'speed':
            self.vel = 5  # Reset velocity to normal
            print("Speed power-up reset")
        elif self.powerup_effect == 'size':
            self.width = self.original_width
            self.height = self.original_height
            self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (self.width, self.height))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            print("Size power-up reset")
        self.powerup_effect = None

# Ball class
class Ball:
    def __init__(self, x, y, image_path, radius=12):
        self.x = x
        self.y = y
        self.radius = radius
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.x_vel = 5
        self.y_vel = 5

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.center = (self.x, self.y)

    def check_collision(self, width, height, paddle_left, paddle_right):
        # Ball collision with top and bottom walls
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.y_vel *= -1

        # Ball collision with paddles
        if self.rect.colliderect(paddle_left.rect) or self.rect.colliderect(paddle_right.rect):
            self.x_vel *= -1
            hit_sound.play()  # Play hit sound on collision

        # Ball out of bounds
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            return True  # Indicates that the ball is out of bounds

        return False

# PowerUp class
class PowerUp:
    def __init__(self, x, y, image_path, effect):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (POWERUP_WIDTH, POWERUP_HEIGHT))
        self.rect = self.image.get_rect(center=(x, y))
        self.effect = effect
        self.x_vel = random.uniform(-2, 2)  # Horizontal speed of the power-up
        self.y_vel = 2  # Vertical speed of the power-up

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.center = (self.x, self.y)

        # Limiting vertical movement within the screen area
        if self.y > HEIGHT - POWERUP_HEIGHT - POWERUP_AREA_MARGIN:
            self.y = HEIGHT - POWERUP_HEIGHT - POWERUP_AREA_MARGIN
            self.y_vel *= -1
        elif self.y < POWERUP_AREA_MARGIN:
            self.y = POWERUP_AREA_MARGIN
            self.y_vel *= -1

        # Limiting horizontal movement within the screen area
        if self.x > WIDTH - POWERUP_WIDTH - POWERUP_AREA_MARGIN or self.x < POWERUP_AREA_MARGIN:
            self.x_vel *= -1

    def apply(self, paddle):
        if self.effect == 'speed':
            paddle.apply_powerup('speed')
        elif self.effect == 'size':
            paddle.apply_powerup('size')
        elif self.effect == 'ball_speed':
            # Ball speed power-up should be applied directly to the Ball class
            game.ball.x_vel *= 1.5
            game.ball.y_vel *= 1.5
        powerup_sound.play()  # Play power-up sound when applied

# Game class
class Game:
    def __init__(self, screen, clock, multiplayer=False, ai_difficulty='medium'):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.paused = False

        # Load images
        self.table_image = pygame.image.load('assets/images/table.png').convert()
        self.table_image = pygame.transform.scale(self.table_image, (WIDTH, HEIGHT))

        self.paddle_left = Paddle(30, HEIGHT // 2, 'assets/images/paddle.jpg')
        self.paddle_right = Paddle(WIDTH - 30, HEIGHT // 2, 'assets/images/paddle.jpg')
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, 'assets/images/ball.jpg')

        self.ai = None
        if not multiplayer:
            self.ai = self.paddle_right  # Using paddle_right as AI
            self.ai_difficulty = ai_difficulty

        self.multiplayer = multiplayer
        self.player1_score = 0
        self.player2_score = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.serve_count = 0
        self.server = 1

        self.powerups = []
        self.powerup_timer = pygame.time.get_ticks()  # Timer to control power-up spawning

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.paused = not self.paused

            self.paddle_left.handle_event(event, player=1)
            self.paddle_right.handle_event(event, player=2)

    def update(self):
        if self.serve_count >= 10:
            self.server = 2 if self.server == 1 else 1
            self.serve_count = 0

        self.ball.move()

        # Ball collision with walls and paddles
        if self.ball.check_collision(WIDTH, HEIGHT, self.paddle_left, self.paddle_right):
            if self.ball.x - self.ball.radius <= 0:
                self.player2_score += 1
                score_sound.play()
                self.check_set_winner()
                self.reset_ball()
                self.paddle_left.reset_powerup()
                self.paddle_right.reset_powerup()
            elif self.ball.x + self.ball.radius >= WIDTH:
                self.player1_score += 1
                score_sound.play()
                self.check_set_winner()
                self.reset_ball()
                self.paddle_left.reset_powerup()
                self.paddle_right.reset_powerup()

        if self.ai:
            self.ai_move()

        self.update_powerups()
        self.check_powerup_collisions()

    def ai_move(self):
        if self.ball.y > self.ai.y:
            self.ai.vel = 5
        elif self.ball.y < self.ai.y:
            self.ai.vel = -5
        else:
            self.ai.vel = 0
        self.ai.move()

    def update_powerups(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.powerup_timer > 5000:  # Spawn a power-up every 5 seconds
            self.spawn_powerups()
            self.powerup_timer = current_time

        for powerup in self.powerups:
            powerup.move()

    def spawn_powerups(self):
        if len(self.powerups) < 5:  # Limit the number of power-ups on screen
            x = random.randint(POWERUP_AREA_MARGIN, WIDTH - POWERUP_WIDTH - POWERUP_AREA_MARGIN)
            y = random.randint(POWERUP_AREA_MARGIN, HEIGHT - POWERUP_HEIGHT - POWERUP_AREA_MARGIN)
            effect = random.choice(['speed', 'size', 'ball_speed'])
            image_path = f'assets/images/{effect}_powerup.png'
            powerup = PowerUp(x, y, image_path, effect)
            self.powerups.append(powerup)

    def check_powerup_collisions(self):
        for powerup in self.powerups:
            if powerup.rect.colliderect(self.paddle_left.rect):
                powerup.apply(self.paddle_left)
                self.powerups.remove(powerup)
            elif powerup.rect.colliderect(self.paddle_right.rect):
                powerup.apply(self.paddle_right)
                self.powerups.remove(powerup)

    def draw(self):
        self.screen.blit(self.table_image, (0, 0))
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        self.ball.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw(self.screen)

        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        font = pygame.font.Font(None, 74)
        player1_text = font.render(str(self.player1_score), True, WHITE)
        player2_text = font.render(str(self.player2_score), True, WHITE)
        self.screen.blit(player1_text, (WIDTH // 4, 10))
        self.screen.blit(player2_text, (WIDTH * 3 // 4, 10))

    def reset_ball(self):
        self.ball.x = WIDTH // 2
        self.ball.y = HEIGHT // 2
        self.ball.x_vel = -self.ball.x_vel  # Change direction
        self.ball.y_vel = random.choice([-5, 5])

    def check_set_winner(self):
        if self.player1_score >= 5:
            self.player1_sets += 1
            self.player1_score = 0
            self.player2_score = 0
        elif self.player2_score >= 5:
            self.player2_sets += 1
            self.player1_score = 0
            self.player2_score = 0

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong Game')
    clock = pygame.time.Clock()
    game = Game(screen, clock, multiplayer=True)
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
