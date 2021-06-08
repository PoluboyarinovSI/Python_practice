"""
Проектирование игры крестики нолики

Объекты и их взаимодействия:
Игрок 1
Игрок 2
Раунд игры
Игровое поле (окно)
Значки: крестик/нолик

Что нужно?

Класс GameRoundManager
-
-- mainloop() - крутится главный цикл

Класс Player

Класс GameField
- cells[]
-- is_game_over()
-- get_cell_state()

Класс Cell
- state (состояния клетки (пустота, крестик, нолик))

Класс GameFieldView (виджет GameField - занимается определением клетки клика)
- load_cell_states
-- get_coords(x, y)

Класс GameWindow
- поле игры
- кнопки управления

"""

import pygame
from pygame.draw import *
from enum import Enum


CELL_SIZE = 50
FPS = 60


class Cell(Enum):
    VOID = 0
    CROSS = 1
    ZERO = 2


class Player:
    """
    Класс игрока, содержащий тип значков и имя.
    """
    def __init__(self, name, cell_type):
        self.name = name
        self.cell_type = cell_type


class GameField:
    def __init__(self):
        self.height = 3
        self.width = 3
        self.cells = [[Cell.VOID] * self.width for i in range(self.height)]


class GameFieldView:
    """
    Виджет игрового поля, который отображает его на экране, выясняет место клика
    """
    def __init__(self, field, screen):
        # загрузить картинки значков клеток
        self._field = field
        self._height = field.height * CELL_SIZE
        self._width = field.width * CELL_SIZE
        self._field_screen = screen
        # отображение первичного поля
        polygon(self._field_screen, [192, 192, 192],
                [((400 - self._width), (300 - self._height)), ((400 + self._width), (300 - self._height)),
                 ((400 + self._width), (300 + self._height)), ((400 - self._width), (300 + self._height))])
        line(self._field_screen, [0, 0, 0], ((400 - self._width), (300 - self._height / 3)),
             ((400 + self._width), (300 - self._height / 3)), width=1)
        line(self._field_screen, [0, 0, 0], ((400 - self._width), (300 + self._height / 3)),
             ((400 + self._width), (300 + self._height / 3)), width=1)
        line(self._field_screen, [0, 0, 0], ((400 - self._width / 3), (300 - self._height)),
             ((400 - self._width / 3), (300 + self._height)), width=1)
        line(self._field_screen, [0, 0, 0], ((400 + self._width / 3), (300 - self._height)),
             ((400 + self._width / 3), (300 + self._height)), width=1)

    def draw(self, i, j, current_player):
        self.i, self. j = i, j
        self.player = current_player[0]
        if self.player.cell_type == Cell.ZERO:
            x = 200 + self.j * CELL_SIZE * 2
            y = 100 + self.i * CELL_SIZE * 2
            circle(self._field_screen, [0, 0, 0], (x, y), CELL_SIZE, width=2)
        elif self.player.cell_type == Cell.CROSS:
            x1 = 150 + self.j * CELL_SIZE * 2
            x2 = 250 + self.j * CELL_SIZE * 2
            y1 = 50 + self.i * CELL_SIZE * 2
            y2 = 150 + self.i * CELL_SIZE * 2
            line(self._field_screen, [0, 0, 0], (x1, y1),
                 (x2, y2), width=2)
            line(self._field_screen, [0, 0, 0], (x1 + 100, y1),
                 (x2 - 100, y2), width=2)

    def check_coords_correct(self, x, y):
        """
        Функция проверки попадания клика игрока в игровое поле
        х - координата клика по оси х
        y - координата клика по оси
        return: True - в случае попадания в игорове пространство, False - в случае промаха
        """
        self.x, self.y = x, y
        if self.x > (400 - self._width) and self.x < (400 + self._width):
            if self.y > (300 - self._height) and self.y < (300 + self._height):
                return True  # TODO: self._height учесть
            else:
                return False
        else:
            return False

    def get_coords(self, x, y):
        """
        Функция определения клетки, по которой был совершен клик мышки
        х - координата клика по оси х
        y - координата клика по оси
        return: i - позиция клетки по вертикали
                j - позиция клетки по горизонтали
        """
        self.x, self.y = x, y
        if self.x > (400 - self._width) and self.x < (400 - self._width / 3):
            if self.y > (300 - self._height) and self.y < (300 - self._height / 3):
                return 1, 1
            elif self.y > (300 - self._height / 3) and self.y < (300 + self._height / 3):
                return 2, 1
            elif self.y > (300 + self._height / 3) and self.y < (300 + self._height):
                return 3, 1
        elif self.x > (400 - self._width / 3) and self.x < (400 + self._width / 3):
            if self.y > (300 - self._height) and self.y < (300 - self._height / 3):
                return 1, 2
            elif self.y > (300 - self._height / 3) and self.y < (300 + self._height / 3):
                return 2, 2
            elif self.y > (300 + self._height / 3) and self.y < (300 + self._height):
                return 3, 2
        elif self.x > (400 + self._width / 3) and self.x < (400 + self._width):
            if self.y > (300 - self._height) and self.y < (300 - self._height / 3):
                return 1, 3
            elif self.y > (300 - self._height / 3) and self.y < (300 + self._height / 3):
                return 2, 3
            elif self.y > (300 + self._height / 3) and self.y < (300 + self._height):
                return 3, 3


class GameRoundManager:
    """
    Менеджер игры, запускающий все процессы.
    """
    def __init__(self, player1: Player, player2: Player):
        self._players = [player1, player2]
        self.current_player = [player1]
        self._current_player_num = 1
        self.field = GameField()
        print('Ходит Игрок №', self._current_player_num)

    def handle_click(self, i, j):
        """
        Функция - обработчик нажатия игороком клика мыши по ячейке.
        i, j - номер строки и столбца ячейки
        """
        player = self.current_player[0]
        if self.field.cells[i - 1][j - 1] == Cell.VOID:
            if self._current_player_num == 1:
                self.field.cells[i - 1][j - 1] = player.cell_type
                return True
            else:
                self.field.cells[i - 1][j - 1] = player.cell_type
                return True
        else:
            return False

    def change_player(self):
        if self._current_player_num % 2 == 0:
            self.current_player.pop(0)
            self._current_player_num = 1
            self.current_player.append(self._players[0])
            print('Ходит Игрок №', self._current_player_num)
        else:
            self.current_player.pop(0)
            self._current_player_num = 2
            self.current_player.append(self._players[1])
            print('Ходит Игрок №', self._current_player_num)

    def check_game_status(self):
        # Проверка выйгрыша крестика
        for c in range(3):
            if self.field.cells[c][0] == self.field.cells[c][1] == self.field.cells[c][2] == Cell.CROSS:
                print('Выйграл игрок - ', self._current_player_num)
                return True
        for c in range(3):
            if self.field.cells[0][c] == self.field.cells[1][c] == self.field.cells[2][c] == Cell.CROSS:
                print('Выйграл игрок - ', self._current_player_num)
                return True
        if self.field.cells[0][0] == self.field.cells[1][1] == self.field.cells[2][2] == Cell.CROSS:
            print('Выйграл игрок - ', self._current_player_num)
            return True
        if self.field.cells[0][2] == self.field.cells[1][1] == self.field.cells[2][0] == Cell.CROSS:
            print('Выйграл игрок - ', self._current_player_num)
            return True
        # Проверка выйгрыша нолика
        for c in range(3):
            if self.field.cells[c][0] == self.field.cells[c][1] == self.field.cells[c][2] == Cell.ZERO:
                print('Выйграл игрок - ', self._current_player_num)
                return True
        for c in range(3):
            if self.field.cells[0][c] == self.field.cells[1][c] == self.field.cells[2][c] == Cell.ZERO:
                print('Выйграл игрок - ', self._current_player_num)
                return True
        if self.field.cells[0][0] == self.field.cells[1][1] == self.field.cells[2][2] == Cell.ZERO:
            print('Выйграл игрок - ', self._current_player_num)
            return True
        if self.field.cells[0][2] == self.field.cells[1][1] == self.field.cells[2][0] == Cell.ZERO:
            print('Выйграл игрок - ', self._current_player_num)
            return True
        # Проверка ничьи
        turn = 0
        for c in range(3):
            for n in range(3):
                if self.field.cells[c][n] != Cell.VOID:
                    turn += 1
        if turn == 9:
            print('Ничья! Конец игры!')
            return True
        return False


class GameWindow:
    """
    Содержит виджет поля, а также менеджер игрового раунда.
    """
    def __init__(self):
        pygame.init()
        # Window
        self._width = 800
        self._height = 600
        self._title = "Crosses & Zeroes"
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)
        player1 = Player("Петя", Cell.CROSS)
        player2 = Player("Вася", Cell.ZERO)
        self._game_manager = GameRoundManager(player1, player2)
        self._field_widget = GameFieldView(self._game_manager.field, self._screen)

    def main_loop(self):
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    if self._field_widget.check_coords_correct(x, y):
                        i, j = self._field_widget.get_coords(x, y)
                        if self._game_manager.handle_click(i, j) == True:
                            self._field_widget.draw(i, j, self._game_manager.current_player)
                            if self._game_manager.check_game_status() == True:
                                finished = True
                            else:
                                self._game_manager.change_player()
            pygame.display.flip()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.main_loop()

if __name__ == "__main__":
    main()