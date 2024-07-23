# ui.py
import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_start_menu(screen):
    screen.fill(BLACK)
    draw_text(screen, "Table Tennis Game", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press 1 for Single Player (Easy)", 32, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press 2 for Single Player (Medium)", 32, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text(screen, "Press 3 for Single Player (Hard)", 32, WIDTH // 2, HEIGHT // 2 + 80)
    draw_text(screen, "Press M for Multiplayer", 32, WIDTH // 2, HEIGHT // 2 + 120)
    pygame.display.flip()

def handle_start_menu_events():
    difficulty = None
    multiplayer = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 'easy'
                    running = False
                elif event.key == pygame.K_2:
                    difficulty = 'medium'
                    running = False
                elif event.key == pygame.K_3:
                    difficulty = 'hard'
                    running = False
                elif event.key == pygame.K_m:
                    multiplayer = True
                    running = False
        pygame.time.wait(100)
    return difficulty, multiplayer
