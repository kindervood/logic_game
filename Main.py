import sys
import pygame
import Game

WINDOW_SIZE = (800, 550)

if __name__ == '__main__':
    pygame.init()
    # размеры окна:
    width, height = WINDOW_SIZE
    screen = pygame.display.set_mode([width, height], flags=pygame.NOFRAME)
    running = True
    game = Game.Game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.get_click(event.pos)

            screen.fill((255, 255, 255))
            game.render(screen)
            running = game.still_running
