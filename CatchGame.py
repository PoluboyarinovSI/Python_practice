# Лабораторная №6. Событийное программирование + декомпозиция программного кода
import pygame
from pygame.draw import *
from random import randint
from math import sqrt

pygame.init()

print('Игра - поймай фигуру')
print('Количество попыток = 7 \nРезультаты отображаются в файле "Results.txt"')
print('Введите имя игрока')
player_name = str(input())

FPS = 1
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():
    """
    Функция создания нового объекта "круг"
    :return: None
    """
    global x, y, r
    color = COLORS[randint(0, 5)]
    x = randint(100, 1110)
    y = randint(100, 800)
    r = randint(20, 100)
    circle(screen, color, (x, y), r)


def new_polygon():
    """
    Функция создания нового объекта "квадрат"
    :return: None
    """
    global x1, y1, width, height
    color = COLORS[randint(0, 5)]
    x1 = randint(100, 1110)
    y1 = randint(100, 800)
    width = randint(20, 100)
    height = randint(20, 100)
    polygon(screen, color, [(x1 - width / 2, y1), (x1 - width / 2, y1 - height),
                            (x1 + width / 2, y1 - height), (x1 + width / 2, y1)])


def new_triangle():
    """
    Функция создания нового объекта "треугольник"
    :return: None
    """
    global x2, y2, width2, height2
    color = COLORS[randint(0, 5)]
    x2 = randint(200, 1000)
    y2 = randint(150, 750)
    width2 = randint(-100, 100)
    height2 = randint(-100, 100)
    polygon(screen, color, [(x2, y2), (x2 + width2, y2),
                            (x2, y2 + height2)])


def click(event):
    """
    Функция обработки нажатия клавиши мыши и подсчета очков
    :param event: Событие модуля Pygame
    :return: возвращает координаты точки нажатия левой кнопки мыши
    """
    global pos_x, pos_y
    A = pygame.mouse.get_pos()
    pos_x = A[0]
    pos_y = A[1]
    return pos_x, pos_y


def check_ball():
    '''
    Функция проверки попадания клика в область круга
    :param x: координата х центра круга
    :param y: координата y центра круга
    :param r: радиус круга
    :param pos_x: координата x нажатия левой кнопки мыши
    :param pos_y: координата y нажатия левой кнопки мыши
    :return: возвращает логическое значение переменной flag_ball, при попадании = True
    '''
    global x, y, r, pos_x, pos_y
    flag_ball = False
    if (pos_x - x) ** 2 + (pos_y - y) ** 2 <= r ** 2:
        flag_ball = True
    return flag_ball


def check_polygon():
    '''
    Функция проверки попадания клика в область прямоугольника
    :param x1: координата x центра прямоугольника
    :param y1: координата y центра прямоугольника
    :param width: ширина прямоугольника
    :param height: высота прямоугольника
    :param pos_x: координата x нажатия левой кнопки мыши
    :param pos_y: координата y нажания левой кнопки мыши
    :return: возвращает логическое значение переменной flag_polygon, при попадании = True
    '''
    global x1, y1, width, height, pos_x, pos_y
    flag_polygon = False
    if (pos_x >= x1 - width) and (pos_x <= x1 + width) and \
            (pos_y >= y1 - height) and (pos_y <= y1 + height):
        flag_polygon = True
    return flag_polygon


def check_triangle():
    '''
    Функция проверки попадания клика в область треугольника
    :param x2: координата x опорной точки треугольника
    :param y2: координата y опорной точки треугольника
    :param width2: параметр ширины треугольника
    :param height2: параметр высоты треугольника
    :param pos_x: координата x нажатия левой кнопки мыши
    :param pos_y: координата y нажатия левой кнопки мыши
    :return: возвращает логическое значение переменной flag_triangle, при попадании = True
    '''
    global x2, y2, width2, height2, pos_x, pos_y
    flag_triangle = False

    a1 = sqrt((pos_x - x2) ** 2 + (pos_y - y2) ** 2)
    b1 = sqrt((pos_x - (x2 + width2)) ** 2 + (pos_y - y2) ** 2)
    c1 = sqrt((x2 - (x2 + width2)) ** 2 + (y2 - y2) ** 2)
    p1 = (a1 + b1 + c1) / 2
    s1 = sqrt(p1 * (p1 - a1) * (p1 - b1) * (p1 - c1))  # Площадь первого малого треугольника

    a2 = sqrt((pos_x - x2) ** 2 + (pos_y - y2) ** 2)
    b2 = sqrt((pos_x - x2) ** 2 + (pos_y - (y2 + height2)) ** 2)
    c2 = sqrt((x2-x2) ** 2 + (y2 - (y2 + height2)) ** 2)
    p2 = (a2 + b2 + c2) / 2
    s2 = sqrt(p2 * (p2 - a2) * (p2 - b2) * (p2 - c2))  # Площадь второго малого треугольника

    a3 = sqrt((pos_x - x2) ** 2 + (pos_y - (y2 + height2)) ** 2)
    b3 = sqrt((pos_x - (x2 + width2)) ** 2 + (pos_y - y2) ** 2)
    c3 = sqrt((x2 - (x2 + width2)) ** 2 + ((y2 + height2) - y2) ** 2)
    p3 = (a3 + b3 + c3) / 2
    s3 = sqrt(p3 * (p3 - a3) * (p3 - b3) * (p3 - c3))  # Площадь третьего малого треугольника

    a4 = sqrt(((x2 - width2) - (x2 - width2)) ** 2 + (y2 - (y2 - height2)) ** 2)
    b4 = sqrt(((x2 - width2) - (x2 + width2)) ** 2 + (y2 - (y2 - height2)) ** 2)
    c4 = sqrt(((x2 - width2) - (x2 + width2)) ** 2 + ((y2 - height2) - (y2 - height2)) ** 2)
    p4 = (a4 + b4 + c4) / 2
    s4 = sqrt(p4 * (p4 - a4) * (p4 - b4) * (p4 - c4))  # Площадь главного треугольника

    if s1 + s2 + s3 <= s4:
        flag_triangle = True
    return flag_triangle


def scoring():
    '''
    Функция подсчета очков при попадании в сформированные фигуры
    :return: None
    '''
    global points, finished
    if check_ball() == True:
        points += 1
        print(f'Игрок {player_name} - Попал в круг + 1 очко! Сумма очков =', points)
        output.write(f'Игрок {player_name} - Попал в круг + 1 очко! Сумма очков = {points}' '\n')
    elif check_polygon() == True:
        points += 2
        print(f'Игрок {player_name} - Попал в прямоугольник + 2 очка! Сумма очков = {points}')
        output.write(f'Игрок {player_name} - Попал в прямоугольник + 2 очка! Сумма очков = {points}' '\n')
    elif check_triangle() == True:
        points += 3
        print(f'Игрок {player_name} - Попал в треугольник + 3 очка! Сумма очков =', points)
        output.write(f'Игрок {player_name} - Попал в треугольник + 3 очка! Сумма очков = {points}' '\n')
    if points >= 21:
        finished = True
        print(f'Игрок {player_name} - Достиг суммы очков =', points)
        output.write(f'Игрок {player_name} - Достиг суммы очков = {points}' '\n')
        print('Конец игры')
        output.write('Конец игры')


output = open('Results.txt', 'w')

pygame.display.update()
clock = pygame.time.Clock()
finished = False
click_try = 0
points = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_try += 1
            print('Попытка номер', click_try)
            click(event)
            check_ball()
            check_polygon()
            check_triangle()
            scoring()
            if click_try == 7:
                finished = True
                print(f'Игрок {player_name} - Исчерпал свои попытки! Сумма очков = {points}')
                output.write(f'Игрок {player_name} - Исчерпал свои попытки! Сумма очков = {points}' '\n')
                print('Конец игры')
                output.write('Конец игры' '\n')
    screen.fill((192, 192, 192))
    new_ball()
    new_polygon()
    new_triangle()
    pygame.display.update()


output.close()
pygame.quit()
input()
