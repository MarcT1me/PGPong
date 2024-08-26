from random import uniform
import numpy as np
import pygame

import scripts
print('\n        entities import  - completed')


class Racquet:

    def __init__(self, screen, correct_player, *, points=0) -> None:
        """ Инициализация ракеток игроков.  \n
        __init__(self, screen, correct_player, *, points=0) -> None

         Создание экземпляра класса 'Racquet':
          1) размеры - от чего в будущем зависит область отскока шарика;
          2) его координаты (x) и (y) - при старте равны середине (x) и (y)-соотв номеру игрока;
          3) логические переменные отвечающие за непрерывное передвижение
          4) очки этого игрока.

        Особенности:
          1. В переменной 'correct_player' указывается номер игрока, начиная с 0
          2. Имеет второй вариант задания ширины - адаптивный (от ширины окна)

        Метод инициализации имеет отладочные 'print'-ы (что неправильно). """

        # размеры ракетки
        self.width: int = 25
        """ # вариант адаптивной ширины
        self.width = screen[0]/50
        print('Использована адаптивная ширина') """
        self.height: float = screen[1]/3
        print('ширина созданной ракетки: ', self.width)
        print('высота созданной ракетки: ', self.height)

        # координаты ракетки
        correct_cords: tuple = (50+self.width, screen[0]-(50+self.width+self.width/2))
        print('конечная координата x: ', correct_cords[correct_player])
        self.x: int = correct_cords[correct_player]-self.width/4
        self.y: int = (screen[1]-self.height)/2

        # логические переменные движения
        self.m_up: bool = False
        self.m_down: bool = False

        # счёт игрока
        self.points: int = points

        print('  entities _racquet_ - create\n')

    def update_racquet(self, screen, frame_rate, speed) -> None:
        """ Обновление позиции ракетки.
        Основывается на логической переменной.
          В кооп-режиме перезаписывается в одноимённом модуле """

        if self.m_up\
                and self.y >= 0 + (speed / (frame_rate / 60)):
            self.y -= speed / (frame_rate / 60)

        elif self.m_down\
                and self.y <= screen[1] - self.height - (speed / (frame_rate / 60)):
            self.y += speed / (frame_rate / 60)


class Ball:

    def __init__(self, screen, speed, frame_rate) -> None:
        """ Инициализация шарика.   \n
        __init__(self, screen, speed) -> None

         Для объявления необходима скорость, чтобы задать начальное направление (случайное).
         Сами проекции на оси рассчитываются по формуле:  'Vx = V * cos(a)'  &  'Vy = V * sin(a).'

         Создание экземпляра класса 'Ball':
          1) размеры шара - только радиус в пикселях;
          2) его координаты (x) и (y);
          3) скорость по осям (x) и (y) - рассчитываются по формуле указанной выше;
          4) состояние отскока False/True - нет/да соответственно

        Метод инициализации имеет отладочные 'print'-ы (что неправильно). """

        # размеры шарика
        self.radius: int = 15

        # координаты шарика
        self.x: int = screen[0]/2
        self.y: int = screen[1]/2

        # функция перезаписи скорости шарика
        def set_bal_speed() -> tuple:
            """ Полная перезапись переменны скоростей.

            Особенность - использует модуль 'NumPy' """
            a_speed = uniform(0, 6)
            x_speed: float = speed*2*np.cos(a_speed)
            y_speed: float = speed*2*np.sin(a_speed)
            print(f'скорость (x: {x_speed / (frame_rate / 60)} y: {y_speed / (frame_rate / 60)})\n'
                  f'угол альфа: {a_speed}')
            return x_speed / (frame_rate / 60), y_speed / (frame_rate / 60)
        # задание переменных
        self.x_speed, self.y_speed = False, False
        # перезаписываю близкие к нулю скорости (в целом 1 раз на 26 перезапусков)
        while (abs(self.y_speed) < 1.5 / (frame_rate / 60)) or (abs(self.x_speed) < 1.5 / (frame_rate / 60)):
            self.x_speed, self.y_speed = set_bal_speed()

        # логические переменные отскока
        self.rebound_x_count = False
        self.rebound_y_count = False

        print('  entities _ball_ - create\n')

    def update_ball(self, screen, player_1, player_2) -> None:
        """ Обновление позиции и направления движения шарика.   \n

         Логика if-elif (использование match-case - излишне):
          1) ракетки игроков
          2) верхняя и нижняя грань
          3) ворота
          4) свободный полёт """

        # отскок от ракетки игроков
        if (((self.y >= player_1.y) and (self.y <= player_1.y+player_1.height)) and
            ((self.x <= player_1.x+player_1.width+(self.radius-5)) and (self.x >= player_1.x-(self.radius-5)))) or\
                (((self.y >= player_2.y) and (self.y <= player_2.y+player_2.height)) and
                 ((self.x <= player_2.x+player_2.width+(self.radius-5)) and (self.x >= player_2.x-(self.radius-5)))):
            self.rebound_x()
            """ Логика player_1: Если мячик находится по координатам Y меньше чем верхняя точка платформы, но
             больше чем её низ(вычисляем зная координату верха и высоту платформы) и при том координата X будит в
             пределах таких же вычислений + радиус мячика (отнимаем 5 пикселей, чтобы казалось что он упругий) """

        # отскок от верхней и нижней граней
        elif (self.y <= 0+(self.radius-5)) or (self.y >= screen[1]-(self.radius-5)):
            self.rebound_y()

        # попадание в левую или правые ворота соответственно
        elif self.x <= 0+(self.radius-5):
            scripts.player_2.points += 1
            scripts.goal = True
            scripts.restart()
        elif self.x >= screen[0]-(self.radius-5):
            scripts.player_1.points += 1
            scripts.goal = True
            scripts.restart()

        # в свободном движении мы больше не отскакиваем > False
        else:
            self.rebound_x_count = False
            self.rebound_y_count = False

        # считаю координату зная скорость
        self.x += self.x_speed
        self.y += self.y_speed

    def rebound_x(self) -> None:
        """ Отскок от горизонтальных поверхностей (x) """
        if not self.rebound_x_count:
            self.x_speed = -self.x_speed
            # мячик отскакивает > True
            self.rebound_x_count = True
            pygame.mixer.music.play(0, 0.15)
        print('move _bole_ - rebound(x)')

    def rebound_y(self) -> None:
        """ Отскок от вертикальных поверхностей (y) """
        if not self.rebound_y_count:
            self.y_speed = -self.y_speed
            # мячик отскакивает > True
            self.rebound_y_count = True
            pygame.mixer.music.play(0, 0.15)
        print('move _bole_ - rebound(y)')


class TextAnnouncement:

    last_size: int = 0
    last_cords: tuple = (0, 0)
    """ Если мы не поменяли координаты, то использую для записи размер и положение прошлых надписей, чтобы
     они не пересекались с новыми """

    def __init__(self, text, *, cords=(10, 0), color='black', text_font='Arial', size=15, pxl=True) -> None:
        """ Инициализация текстовой надписи.    \n
        __init__(self, text, *, cords=(10, 10), color=(0, 0, 0), text_type='Arial', size=15) -> None

         Стандарт - каждая новая надпись добавляется в левый верхний угол по вертикали,
         учитывая размеры, чтобы полностью поместиться. Чтобы изменить это, необходимо
         явно указать на его координаты.

         Создание второстепенных переменных класса 'TextAnnouncement':
          1) текст - указывается обязательно;
          2) размер шрифта;
          3) координаты - указываются (x, y) (зависит от стандартных координат);
          4) цвет, указывается текстом, а не RGB.

        Создание самого текста происходит в PyGame, но стиль сохраняется в переменных.

        Метод инициализации имеет отладочные 'print'-ы (что неправильно). """

        # главный текст (changeable)
        self.message: str = str(text)

        # вычисление координат
        self.x: int = cords[0]
        # если я не указывал координату использую стандартны значения
        if cords == (10, 0):
            self.y: int = TextAnnouncement.last_cords[1] + TextAnnouncement.last_size+5
            TextAnnouncement.last_size = size
            TextAnnouncement.last_cords = (self.x, self.y)
        # если менял, указываю полученную координату
        else:
            self.y: int = cords[1]

        # стиль текста
        self.color: str = color
        self.pixel = pxl
        # стиль нужный для создания переменной
        self.text_font: str = text_font
        self.size: int = size

        # Создание переменной класса текста (PyGame)
        self.text = pygame.font.SysFont(self.text_font, self.size)

        print('  entities _text_ - written\n')

    def write_text(self, window, *, top=False) -> None:
        """ Зарисовка текста на очищенном 'холсте' """

        match top:
            case False:
                fin_text = self.text.render(f'{self.message}', self.pixel, self.color)
                window.blit(fin_text, (self.x, self.y))
            case True:
                fin_text = self.text.render(f'{self.message}', self.pixel, self.color)
                window.blit(fin_text, (self.x - fin_text.get_width()//2, self.y - fin_text.get_height()//2-100))


class Square:

    def __init__(self, *, width=3840, height=2160, x=3840/2, y=2160/2, color=(0, 0, 0)) -> None:
        """ Инициализация условного квадрата.   \n
        __init__(self, *, width=3840, height=2160, cords=(0, 0), color=(0, 0, 0)) -> None

         Условный потому что в зависимости от переданных переменных и их количества его форма может изменяться и объект
         класса 'Square' становится линией/квадратом/прямоугольником причём, опять же в зависимости от указанных
         переменных, может, как проходить насквозь весь экран, так и оставаться в его рамках.

         Создание экземпляра класса 'Square':
          1) размеры квадрата - ширина и высота (стандартные значения подходят разрешению экрана;
          2) его координаты (x, y);
          3) цвет квадрата в формате RGB - готовый картеж.

        Особенности:
          1. Чтобы получилась линия на всё поле, нужно указать либо 'width', либо 'height'.
          2. Если поменять координаты, то квадрат полностью займёт участок экрана >указанной координаты.

        Метод инициализации имеет отладочные 'print'-ы (что неправильно). """

        self.width: int = width
        self.height: int = height
        self.x: float = x-width/2
        self.y: float = y-height/2
        self.color: tuple = color

        print('  entities _rect_ - draw\n')

    def draw_rect(self, window) -> None:
        """ Зарисовка условного квадрата на очищенном 'холсте' """
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))


print('        entities - completed\n')
