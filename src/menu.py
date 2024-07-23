import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.options = ['Single Player', 'Multiplayer']
        self.difficulties = ['easy', 'medium', 'hard']
        self.selected_option = 0
        self.selected_difficulty = 1
        self.selection_stage = 'mode'  # Tracks if we're selecting mode or difficulty

    def display_menu(self):
        while True:
            self.screen.fill(BLACK)
            title_text = self.font.render("Table Tennis Game", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            self.screen.blit(title_text, title_rect)

            if self.selection_stage == 'mode':
                for i, option in enumerate(self.options):
                    color = WHITE if i == self.selected_option else (100, 100, 100)
                    option_text = self.font.render(option, True, color)
                    option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 100))
                    self.screen.blit(option_text, option_rect)
            elif self.selection_stage == 'difficulty':
                difficulty_text = self.font.render("Select Difficulty", True, WHITE)
                difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
                self.screen.blit(difficulty_text, difficulty_rect)

                for i, difficulty in enumerate(self.difficulties):
                    color = WHITE if i == self.selected_difficulty else (100, 100, 100)
                    difficulty_text = self.font.render(difficulty, True, color)
                    difficulty_rect = difficulty_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 100))
                    self.screen.blit(difficulty_text, difficulty_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if self.selection_stage == 'mode':
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            self.selection_stage = 'difficulty'
                    elif self.selection_stage == 'difficulty':
                        if event.key == pygame.K_UP:
                            self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
                        elif event.key == pygame.K_DOWN:
                            self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
                        elif event.key == pygame.K_RETURN:
                            multiplayer = self.selected_option == 1
                            return self.difficulties[self.selected_difficulty], multiplayer

            pygame.display.flip()
