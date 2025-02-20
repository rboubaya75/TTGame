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

# Initialize Pygame
pygame.init()
pygame.font.init()

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
        self.powerup_end_time = None

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
            self.vel *= 5
            self.powerup_effect = 'speed'
            self.powerup_end_time = None  # Power-up lasts until point is scored
            print(f"Speed power-up applied: Velocity is now {self.vel}")
        elif effect == 'size':
            self.width = int(self.original_width * 2)
            self.height = int(self.original_height * 2)
            self.image = pygame.transform.scale(pygame.image.load(self.image_path).convert_alpha(), (self.width, self.height))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.powerup_effect = 'size'
            self.powerup_end_time = None  # Power-up lasts until point is scored
            print("Size power-up applied")

    def update(self):
        # No need to check for powerup_end_time as power-ups last until point is scored
        pass

    def reset_powerup(self):
        if self.powerup_effect == 'speed':
            self.vel = 2 # Reset velocity to normal
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
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.y_vel *= -1

        if self.rect.colliderect(paddle_left.rect):
            self.x_vel *= -1
            pygame.mixer.Sound('assets/sounds/hit.wav').play()
        elif self.rect.colliderect(paddle_right.rect):
            self.x_vel *= -1
            pygame.mixer.Sound('assets/sounds/hit.wav').play()

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
        paddle.apply_powerup(self.effect)

# Game class
class Game:
    def __init__(self, screen, clock, multiplayer=False, difficulty='amateur'):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.paused = False

        # Load images
        self.table_image = pygame.image.load('assets/images/table.png').convert()
        self.table_image = pygame.transform.scale(self.table_image, (WIDTH, HEIGHT))

        self.paddle_left = Paddle(30, HEIGHT // 2, 'assets/images/paddle.png')
        self.paddle_right = Paddle(WIDTH - 30, HEIGHT // 2, 'assets/images/paddle.png')
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, 'assets/images/ball.png')

        self.ai = None
        if not multiplayer:
            self.ai = self.paddle_right  # Using paddle_right as AI

        self.multiplayer = multiplayer
        self.difficulty = difficulty
        self.player1_score = 0
        self.player2_score = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.serve_count = 0
        self.server = 1

        self.powerups = []
        self.powerup_timer = pygame.time.get_ticks()  # Timer to control power-up spawning
        self.powerup_spawned = False

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
                elif event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.paused = False
                    else:
                        self.running = False  # Quit the game

            self.paddle_left.handle_event(event, player=1)
            if self.multiplayer:
                self.paddle_right.handle_event(event, player=2)

    def update(self):
        self.ball.move()
        self.ball.check_collision(WIDTH, HEIGHT, self.paddle_left, self.paddle_right)
        self.paddle_left.move()
        self.paddle_right.move()

        if not self.multiplayer and self.ai:
            self.ai_move()

        self.update_powerups()
        self.check_powerup_collisions()

        if self.ball.x - self.ball.radius <= 0:
            self.player2_score += 1
            self.check_set_winner()
            self.reset_ball()
            self.paddle_left.reset_powerup()
            self.paddle_right.reset_powerup()
            self.powerups.clear()

        if self.ball.x + self.ball.radius >= WIDTH:
            self.player1_score += 1
            self.check_set_winner()
            self.reset_ball()
            self.paddle_left.reset_powerup()
            self.paddle_right.reset_powerup()
            self.powerups.clear()

        self.paddle_left.update()
        self.paddle_right.update()

    def ai_move(self):
        speed = {'amateur': 3, 'professional': 7 }.get(self.difficulty, 3)
        if self.ball.y < self.paddle_right.y:
            self.paddle_right.y -= speed
        elif self.ball.y > self.paddle_right.y:
            self.paddle_right.y += speed

        if self.paddle_right.y < self.paddle_right.height // 2:
            self.paddle_right.y = self.paddle_right.height // 2
        elif self.paddle_right.y > HEIGHT - self.paddle_right.height // 2:
            self.paddle_right.y = HEIGHT - self.paddle_right.height // 2

    def check_set_winner(self):
        if self.player1_score >= 11 and self.player1_score > self.player2_score:
            self.player1_sets += 1
            self.reset_scores()
        elif self.player2_score >= 11 and self.player2_score > self.player1_score:
            self.player2_sets += 1
            self.reset_scores()

        if self.player1_sets >= 3 or self.player2_sets >= 3:
            self.running = False

    def reset_scores(self):
        self.player1_score = 0
        self.player2_score = 0

    def reset_ball(self):
        self.ball.x = WIDTH // 2
        self.ball.y = HEIGHT // 2
        self.ball.x_vel *= random.choice([-1, 1])
        self.ball.y_vel *= random.choice([-1, 1])

    def update_powerups(self):
        for powerup in self.powerups:
            powerup.move()
            if powerup.y > HEIGHT:
                self.powerups.remove(powerup)

        if pygame.time.get_ticks() - self.powerup_timer > 10000:
            self.spawn_powerup()
            self.powerup_timer = pygame.time.get_ticks()

    def spawn_powerup(self):
        x = random.randint(POWERUP_AREA_MARGIN + POWERUP_WIDTH // 2, WIDTH - POWERUP_AREA_MARGIN - POWERUP_WIDTH // 2)
        y = POWERUP_AREA_MARGIN
        effect = random.choice(['speed', 'size'])
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
        self.draw_scores()
        self.draw_powerups()
        if self.paused:
            self.draw_pause_menu()
        pygame.display.flip()

    def draw_scores(self):
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.player1_score), True, WHITE)
        self.screen.blit(text, (250, 10))
        text = font.render(str(self.player2_score), True, WHITE)
        self.screen.blit(text, (510, 10))

        font = pygame.font.Font(None, 50)
        text = font.render(f'Sets: {self.player1_sets} - {self.player2_sets}', True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    def draw_powerups(self):
        for powerup in self.powerups:
            powerup.draw(self.screen)

    def draw_pause_menu(self):
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 60))

        font = pygame.font.Font(None, 50)
        options = ["Resume", "Main Menu"]
        for i, option in enumerate(options):
            color = WHITE
            text = font.render(option, True, color)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + i * 40))

    def handle_pause_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.paused_selection = (self.paused_selection - 1) % 2
            elif event.key == pygame.K_DOWN:
                self.paused_selection = (self.paused_selection + 1) % 2
            elif event.key == pygame.K_RETURN:
                if self.paused_selection == 0:  # Resume
                    self.paused = False
                elif self.paused_selection == 1:  # Main Menu
                    self.running = False

# Menu class
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.current_selection = 0
        self.menu_options = ['Single Player', 'Multiplayer', 'Quit']
        self.difficulty_levels = ['amateur', 'professional']
        self.current_difficulty = 0  # Default to 'amateur'
        self.mode_selection = None  # Keeps track of whether we are in mode selection or difficulty selection

    def draw(self):
        self.screen.fill(BLACK)
        title_font = pygame.font.Font(None, 100)
        title_text = title_font.render("PING PANG", True, WHITE)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 150))

        if self.mode_selection is None:
            for i, option in enumerate(self.menu_options):
                color = WHITE if i == self.current_selection else (100, 100, 100)
                text = self.small_font.render(option, True, color)
                self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + i * 80))
        elif self.mode_selection == 'difficulty':
            difficulty_text = self.small_font.render(f"Difficulty: {self.difficulty_levels[self.current_difficulty]}", True, WHITE)
            self.screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, HEIGHT // 2 + 80))
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.mode_selection is None:
                    self.current_selection = (self.current_selection + 1) % len(self.menu_options)
                elif self.mode_selection == 'difficulty':
                    self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulty_levels)
            elif event.key == pygame.K_UP:
                if self.mode_selection is None:
                    self.current_selection = (self.current_selection - 1) % len(self.menu_options)
                elif self.mode_selection == 'difficulty':
                    self.current_difficulty = (self.current_difficulty - 1) % len(self.difficulty_levels)
            elif event.key == pygame.K_RETURN:
                self.select_option()
            elif event.key == pygame.K_ESCAPE:
                if self.mode_selection is not None:
                    self.mode_selection = None  # Go back to main menu

    def select_option(self):
        if self.mode_selection is None:
            if self.current_selection == 0:  # Single Player
                self.mode_selection = 'difficulty'
            elif self.current_selection == 1:  # Multiplayer
                self.mode_selection = 'difficulty'
            elif self.current_selection == 2:  # Quit
                pygame.quit()
                sys.exit()
        elif self.mode_selection == 'difficulty':
            difficulty = self.difficulty_levels[self.current_difficulty]
            multiplayer = self.current_selection == 1
            game = Game(self.screen, pygame.time.Clock(), multiplayer, difficulty)
            game.run()
            self.mode_selection = None
            self.current_selection = 0

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    menu = Menu(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            menu.handle_event(event)
        
        menu.draw()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
