import pygame

CELL_SIZE = (50, 30)
TABLE_SIZE = (5, 10)
TABLE_INDENT = (300, 100)


class Game:
    def __init__(self):
        self.cell_width, self.cell_height = CELL_SIZE
        self.table_width, self.table_height = TABLE_SIZE
        self.left, self.top = TABLE_INDENT

    def render(self, screen):
        for x in range(self.table_width):
            for y in range(self.table_height):
                pygame.draw.rect(screen, 'black',
                                 (self.cell_width * x + self.left, self.cell_height * y + self.top,
                                  self.cell_width, self.cell_height), 1)

        pygame.display.flip()




