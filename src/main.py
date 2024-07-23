import pygame
from game import Game
from menu import Menu
from settings import WIDTH, HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Table Tennis Game")
    clock = pygame.time.Clock()
    
    menu = Menu(screen)
    ai_difficulty, multiplayer = menu.display_menu()

    game = Game(screen, clock, ai_difficulty, multiplayer)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
