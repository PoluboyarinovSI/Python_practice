# Объектно-ориентированное программирование. Игра - платформа
"""
Для чего нужно:
 - ограничить область видимости (имен)
 - сузить, очертить решаемую задачу
 - документировать задачу
Что для этого существует:
 - функции
 - модули
 - классы
Объект имеет свойства и класс (тип объектов).
Класс определяет набор свойств и определеяет поведение, определяет конструирование.
Объект - это экземпляр класа.
UML - объединенный язык моделирования:
 - диаграммка классов

S.O.L.I.D. - принцип программирования
S - single responsibility principle (принцип единственной отвественности класса)
O -
L - liskov substitution principle (подстановочный принцип Барбары Лисков)
I -
D -

class Base:
    def __intit__(self, x):
        self.x = x

    def show(self):
        print('Base', self.x)

class Derivative(Base)
    def __init__(self):
        super().__init__(20) # явный вызов конструктора: - возвращает надкласс
        self.name = ""

"""
from tkinter import *
import time
import random

# Задается новые объект - окно с игровым полем
tk = Tk()
tk.title('Game')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
# Создается новый холст
canvas = Canvas(tk, width=500, height=400)
canvas.pack()
tk.update()

class Ball:
    # конструктор, который вызывается в момент создания нового объекта класса Ball
    def __init__(self, canvas, paddle, score, color):
        # задаются параметры объекта, передаваемые в скобках в момент создания объекта
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        # создается овал с радиусом 15
        self.id = canvas.create_oval(10,10,25,25, fill=color)
        # объект помещается в точку (245, 100)
        self.canvas.move(self.id, 245, 100)
        # задается список возможных направлений для старта
        starts = [-2, -1, 1, 2]
        # перемешивание направлений
        random.shuffle(starts)
        # выбирается первое случайное направление
        self.x = starts[0]
        # мяч падает вниз
        self.y = -2
        # мяч узнает своют высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # свойство, которое отвечает
        self.hit_bottom = False

    def hit_paddle(self, pos):
        '''
        Функция обработки касания платформы
        :param pos: координаты мяча
        :return: True - в случае, если мяч коснулся платформы
        '''
        # определение координат платформы через объект paddle (платформа)
        paddle_pos = self.canvas.coords(self.paddle.id)
        # проверка совпадения координат мяча с координатами платформы
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.score.hit()
                return True
        return False

    def draw(self):
        # установка шарика на заданные координаты x и y
        self.canvas.move(self.id, self.x, self.y)
        # получаем координаты шарика
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 2
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 120, text='Вы проиграли', fill='red')
        if self.hit_paddle(pos) == True:
            self.y = -2
        if pos[0] <= 0:
            self.x = 2
        if pos[2] >= self.canvas_width:
            self.x = -2

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,100,10, fill=color)
        starts_1 = [40,60,90,120,150,180,200]
        random.shuffle(starts_1)
        self.starting_point_x = starts_1[0]
        self.canvas.move(self.id, self.starting_point_x, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.started = True

    def turn_right(self, event):
        self.x = 2

    def turn_left(self, event):
        self.x = -2

    def start_game(self, event):
        self.started = True

    # метод который отвечает за движение платформы
    def draw(self):
        # смещение платформы на заданное количество пикселей
        self.canvas.move(self.id, self.x, 0)
        # получение координат холста
        pos = self.canvas.coords(self.id)
        # проверка границ
        if pos[0] <= 0:
            # остановка перемещения
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0


# Описание класса Score, который отвечает за отображение счетов
class Score:
    # конструктор
    def __init__(self, canvas, color):
        # в самом начале счет равен нулю
        self.score = 0
        # использование холста
        self.canvas = canvas
        # создается надпись, которая показывает текущий счет, делаем его нужного цвета
        self.id = canvas.create_text(450, 10, text=self.score, font=('Arial', 15), fill=color)
    def hit(self):
        # увеличиваем счет на единицу
        self.score += 1
        # пишем новое значение счета
        self.canvas.itemconfig(self.id, text=self.score)


score = Score(canvas, 'green')
paddle = Paddle(canvas, 'White')
ball = Ball(canvas, paddle, score, 'red')

while 1:
    # начало движения платформы
    if ball.hit_bottom == False and paddle.started == True:
        # двигаем шарик
        ball.draw()
        # двигаем платформу
        paddle.draw()
    tk.update_idletasks()
    # обновляем игровое поле, и смотрим за тем, чтобы все, что должно быть сделано
    tk.update()
    time.sleep(0.01)
