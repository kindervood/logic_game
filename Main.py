import sys
import pygame
import Game

WINDOW_SIZE = (800, 700)

if __name__ == '__main__':
    pygame.init()
    # размеры окна:
    width, height = WINDOW_SIZE
    screen = pygame.display.set_mode([width, height])
    running = True
    game = Game.Game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.fill((255, 255, 255))
            game.render(screen)
