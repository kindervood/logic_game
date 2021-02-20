import pygame
import os
import sys
import random

CELL_SIZE = (50, 30)
TABLE_SIZE = (5, 11)
TABLE_INDENT = (300, 100)
DESCRIPTION1 = '''Компьютер загадал 5 неповторяющихся цветов.\n
                                    Попробуй угадать менее, чем за 10 ходов.\n
                                    Ты можешь узнать правильность твоих \n
                                    размышлений по цвету соответсвующих клеток \n
                                    в разделе Результат хода.\n
                                    Если клетка белая, значит цвет выбран верный,  \n
                                    если черная, то подумай и поменяй цвет в своем \n
                                    следующем ходе. Чтобы выбрать цвет, щелкай \n
                                    по клетке несколько раз, пока не выбран нужный \n
                                    цвет. Чтобы узнать резульаты хода, закрась \n
                                    все ячейки хода и нажми кнопку Проверить.'''.split('\n')

DESCRIPTION2 = '''Компьютер загадал 5 цветов (могут повторятся).\n
                                    Попробуй угадать менее, чем за 10 ходов.\n
                                    Ты можешь узнать правильность твоих \n
                                    размышлений по цвету соответсвующих клеток \n
                                    в разделе Результат хода.\n
                                    Если клетка белая, значит цвет выбран верный,  \n
                                    если черная, то подумай и поменяй цвет в своем \n
                                    следующем ходе. Чтобы выбрать цвет, щелкай \n
                                    по клетке несколько раз, пока не выбран нужный \n
                                    цвет. Чтобы узнать резульаты хода, закрась \n
                                    все ячейки хода и нажми кнопку Проверить.'''.split('\n')


class Game:
    def __init__(self):
        self.cell_width, self.cell_height = CELL_SIZE
        self.table_width, self.table_height = TABLE_SIZE
        self.left, self.top = TABLE_INDENT

        self.key_endgame = False
        self.game_started = False
        self.level = 1
        self.res = [0, 0, 0, 0, 0]

        # загрузка картинок
        self.arrow_right = self.load_image("blue_arrow_right.jpg")
        self.image_arrow_right = pygame.transform.scale(self.arrow_right, (50, 30))
        self.arrow_left = self.load_image("blue_arrow_left.jpg")
        self.image_arrow_left = pygame.transform.scale(self.arrow_left, (50, 30))

        self.changing_btn = self.load_image("start.jpg")
        self.image_changing_btn = pygame.transform.scale(self.changing_btn, (125, 50))
        self.changing_btn_geometry = (625, 425, 100, 50)

        self.level = self.load_image("level.jpg")
        self.image_level = pygame.transform.scale(self.level, (100, 50))
        self.level_geometry = (25, 25, 115, 50)

        self.re = self.load_image("restart.jpg")
        self.image_restart = pygame.transform.scale(self.re, (100, 50))
        self.re_geometry = (690, 25, 100, 50)

        # определение цветов и таблицы нажатий
        self.colors = {
            0: 'white', 1: 'blue', 2: 'green', 3: 'yellow', 4: 'red', 5: 'grey'
        }
        self.click_counts = [[0 for _ in range(self.table_width)] for _ in range(self.table_height)]
        self.turn = 1

        # обьявление основных элементов окна
        self.status_text = 'Нажми кнопку Начать'
        self.status_geometry = (150, 25, 525, 50)

        self.description_text = DESCRIPTION1
        self.description_geometry = (25, 100, 255, 250)

        self.turn_text = 'Ваш ход'
        self.turn_geometry = (600, 360, 100, 50)

        self.res_text = 'Результат хода'

    def render(self, screen):
        # отрисовка таблицы(поля для игры)
        for x in range(self.table_width):
            for y in range(self.table_height):
                # отрисовка цветов клеток в зависимости от того сколько раз кликнули
                cell = self.click_counts[y][x]
                pygame.draw.rect(screen, self.colors[cell],
                                 (self.cell_width * x + self.left + 1,
                                  self.cell_height * (y - 1) + self.top + 1,
                                  self.cell_width - 2, self.cell_height - 1))
                # сетка таблицы
                pygame.draw.rect(screen, 'black',
                                 (self.cell_width * x + self.left, self.cell_height * y + self.top,
                                  self.cell_width, self.cell_height), 1)

        for i in range(5):
            c = ['white', 'black']
            pygame.draw.rect(screen, c[self.res[i]],
                             (self.cell_width * i + self.left + 1,
                              self.cell_height * 10 + self.top + 1,
                              self.cell_width - 2, self.cell_height - 2))

        # отрисовка статуса игры
        pygame.draw.rect(screen, 'black',
                         self.status_geometry, 1)
        screen.blit(self.text_format(self.status_text, 40),
                    (self.status_geometry[0] + 10, self.status_geometry[1] + 3))

        # отрисовка описания
        pygame.draw.rect(screen, 'black',
                         self.description_geometry, 1)
        for i in range(len(self.description_text)):
            screen.blit(self.text_format(self.description_text[i].strip(), 13), (30, 110 + 10 * i))

        # отрисовка уровня
        screen.blit(self.image_level, (self.level_geometry[0:2]))

        # отрисовка начать заново
        screen.blit(self.image_restart, (self.re_geometry[0:2]))

        # отрисовка начать/проверить
        screen.blit(self.image_changing_btn, (self.changing_btn_geometry[0:2]))

        # отрисовка ваш ход и стрелки для него
        screen.blit(self.text_format(self.turn_text, 20), (620, 360 - 30 * (self.turn - 1) + 15))
        screen.blit(self.image_arrow_left, (560, 360 - 30 * (self.turn - 1) + 10))

        # отрисовка результат и стрелки для него
        screen.blit(self.text_format(self.res_text, 20), (90, 400))
        screen.blit(self.image_arrow_right, (230, 400))

        pygame.display.flip()

    def text_format(self, message, text_size, text_color='black', shrift='arial'):
        # функция для преобразования текста
        f2 = pygame.font.SysFont(shrift, text_size)
        text2 = f2.render(message, False, text_color)
        return text2

    def load_image(self, name):
        # функция для загрузки картинок
        fullname = os.path.join(name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    def get_click(self, mouse_pos):
        # функция обработки нажатия мыши
        # обработка нажатия на Начать
        changing_btn_pressed = pygame.Rect(self.changing_btn_geometry).collidepoint(mouse_pos)
        if changing_btn_pressed and self.game_started:
            if 0 not in set(self.click_counts[self.table_height - self.turn]):
                self.res = [0, 0, 0, 0, 0]
                self.res = []
                self.status_text = 'Выбери цвета'
                self.check()
            else:
                self.status_text = 'Не все цвета заполнены'
        if changing_btn_pressed and not self.game_started:
            self.game_started = True
            self.changing_btn = self.load_image("check.jpg")
            self.image_changing_btn = pygame.transform.scale(self.changing_btn, (125, 50))
            self.restart('Выбери цвета')
        # нажатие на кнопку играть заново
        re_btn_pressed = pygame.Rect(self.re_geometry).collidepoint(mouse_pos)
        if re_btn_pressed:
            self.restart('Выбери цвета')

        level_btn_pressed = pygame.Rect(self.level_geometry).collidepoint(mouse_pos)
        if level_btn_pressed:
            if self.level == 1:
                self.level = 2
                self.description_text = DESCRIPTION2
            else:
                self.level = 1
                self.description_text = DESCRIPTION1
            self.restart(f'Уровень сложности изменен на {self.level}')

        if self.game_started:
            x, y = mouse_pos[0] - self.left, mouse_pos[1] - self.top
            # определение х-координаты клетки в зависимости от хода
            if 0 < x < 250 and 300 - 30 * self.turn < y < 300 - 30 * (self.turn - 1):
                x_table = x // 50 + 1
                self.click_counts[self.table_height - self.turn][x_table - 1] += 1
                self.click_counts[self.table_height - self.turn][x_table - 1] %= 6

    def check(self):
        # функия проверки победы/поражения, анализа для результата
        for i in range(5):
            if self.comp_choose[i] == self.click_counts[self.table_height - self.turn][i]:
                self.res.append(0)
            else:
                self.res.append(1)

        if self.res == [0, 0, 0, 0, 0]:
            self.status_text = 'Ты выиграл!'
            self.key_endgame = True
        if self.turn == 10 and set(self.res) != {0}:
            self.status_text = 'Ты проиграл!'
            self.key_endgame = True
        if self.turn != 10 and not self.key_endgame:
            self.turn += 1

    # функция рестарта
    def restart(self, text):
        self.res = [0, 0, 0, 0, 0]
        self.turn = 1
        self.click_counts = [[0 for _ in range(self.table_width)] for _ in range(self.table_height)]
        self.key_endgame = False
        self.status_text = text
        if self.level == 1:
            self.comp_choose = [1, 2, 3, 4, 5]
            random.shuffle(self.comp_choose)
        else:
            self.comp_choose = [int(random.randint(1, 5)) for _ in range(5)]
