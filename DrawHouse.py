# Лабораторная №5. Декомпозиция программного кода и структурное программирование
import pygame
from pygame.draw import *
from random import randint

print('Введите полную ширину дома')
width = int(input())
print('Введите полную высоту дома')
height = int(input())

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

def main(width, height):
    x, y, = 200, 300
    draw_house(x, y, width, height)


def draw_house(x, y, width, height):
    """
    Функция рисует домик полной ширины width и высоты height от опорной точки (x, y),
    которая находится в середине нижней точки фундамента
    :param x: координата x середины домика
    :param y: координата y низа фундамента
    :param width: полная ширина домика (фундамент или вылеты крыши включены)
    :param height: полная высота
    :return: None
    """
    print('рисую домик', x, y, width, height)
    foundation_height = 0.1 * height
    walls_height = 0.7 * height
    walls_width = 0.8 * width
    roof_height = height - foundation_height - walls_height
    window_height = walls_height / 4
    window_width = walls_width / 4

    draw_house_foundation(x, y, width, foundation_height)
    draw_house_walls(x, y - foundation_height, walls_width, walls_height)
    draw_house_roof(x, y - foundation_height - walls_height, width, roof_height)
    draw_house_windows_left(x - walls_width / 4, y - foundation_height - walls_height / 3,
                            window_width, window_height)
    draw_house_windows_right(x + walls_width / 4, y - foundation_height - walls_height / 3,
                            window_width, window_height)

def draw_house_foundation(x, y, width, height):
    """
    Функция рисует основание домика полной ширины width и высоты foundation_height от опорной точки (x, y),
    которая находится в середине нижней точки фундамента
    :param x: координата x середины домика
    :param y: координата y низа фундамента
    :param width: полная ширина домика (фундамент или вылеты крыши включены)
    :param height: полная высота
    :return: None
    """
    print('рисую основание', x, y, width, height)
    polygon(screen, (randint(0, 255), randint(0, 255), randint(0, 255)),
            [(x - width / 2, y), (x - width / 2, y - height),
             (x + width / 2, y - height), (x + width / 2, y)])

def draw_house_walls(x, y, width, height):
    """
    Функция рисует стены домика ширины walls_width и высоты walls_height от опорной точки (x, y),
    которая находится в середине нижней точки фундамента
    :param x: координата x середины домика
    :param y: координата y низа фундамента
    :param width: полная ширина домика (фундамент или вылеты крыши включены)
    :param height: полная высота
    :return: None
    """
    print('рисую стены', x, y, width, height)
    polygon(screen, (randint(0, 255), randint(0, 255), randint(0, 255)),
            [(x - width / 2, y), (x - width / 2, y - height),
             (x + width / 2, y - height), (x + width / 2, y)])

def draw_house_roof(x, y, width, height):
    """
    Функция рисует крышу домика полной ширины width и высоты roof_height от опорной точки (x, y),
    которая находится в середине нижней точки фундамента
    :param x: координата x середины домика
    :param y: координата y низа фундамента
    :param width: полная ширина домика (фундамент или вылеты крыши включены)
    :param height: полная высота
    :return: None
    """
    print('рисую крышу', x, y, width, height)
    polygon(screen, (randint(0, 255), randint(0, 255), randint(0, 255)),
            [(x - width / 2, y), (x + width / 2, y), (x, y - height)])


def draw_house_windows_left(x, y, width, height):
    """
    Функция рисует левое окно домика ширины window_width и высоты window_height от опорной точки (x, y),
    которая находится в середине нижней точки фундамента
    :param x: координата x середины домика
    :param y: координата y низа фундамента
    :param width: полная ширина домика (фундамент или вылеты крыши включены)
    :param height: полная высота
    :return: None
    """
    print('Рисую левое окно', x, y, width, height)
    polygon(screen, (255, 255, 0),
            [(x - width / 2, y), (x - width / 2, y - height),
             (x + width / 2, y - height), (x + width / 2, y)])
    line(screen, (0, 0, 0), (x, y), (x, y - height), 1)
    line(screen, (0, 0, 0), (x - width / 2, y - height / 2), (x + width / 2, y - height / 2), 1)


def draw_house_windows_right(x, y, width, height):
    """
    Функция рисует правое окно домика ширины window_width и высоты window_height от опорной точки (x, y),
    которая находится в середине нижней точки фундамента
    :param x: координата x середины домика
    :param y: координата y низа фундамента
    :param width: полная ширина домика (фундамент или вылеты крыши включены)
    :param height: полная высота
    :return: None
    """
    print('Рисую правое окно', x, y, width, height)
    polygon(screen, (255, 255, 0),
            [(x - width / 2, y), (x - width / 2, y - height),
             (x + width / 2, y - height), (x + width / 2, y)])
    line(screen, (0, 0, 0), (x, y), (x, y - height), 1)
    line(screen, (0, 0, 0), (x - width / 2, y - height / 2), (x + width / 2, y - height / 2), 1)

main(width, height)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


pygame.quit()
