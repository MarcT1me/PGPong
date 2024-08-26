import pygame
import sys

import entities

print('        scripts import  - completed\n\n')


""" Глобальные переменные игры:
 1) экран
 2) цветовая схема
 3) логика главного цикла (через импорт в main файле)
 4) создание сущностей
"""
pygame.init()
pygame.font.init()

# Экран и все исходные
screen_size: dict = {'4k': (3840, 2160),
                     '2k': (2560, 1440),
                     'HD': (1920, 1010),
                     '720p': (1280, 720),
                     '480p': (640, 480)}
screen_resolution: str = '720p'
screen: tuple = screen_size[screen_resolution]

# Цвета RGB
colors: dict = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'BLACK-GREY': (255/4, 255/4, 255/4),
    'GRAY': (255/3, 255/3, 255/3),
    'LIGHT-GRAY': (255/2, 255/2, 255/2)
}

# Глобальные переменные главной функции
clock = pygame.time.Clock()
FPS: int = 60
aggregate_fps_count = 'loading FPS'
aggregate_fps_text = entities.TextAnnouncement(aggregate_fps_count)
start: bool = True
pause: bool = False
goal: bool = False
help_count = True

# Переменные игровых сущностей
speed: int = 6

player_1 = entities.Racquet(
    screen,
    0
)
player_2 = entities.Racquet(
    screen,
    1
)
ball = entities.Ball(
    screen,
    speed,
    FPS
)
# счёт игроков
player1_score = entities.TextAnnouncement(player_1.points,
                                          color='blue', size=75, cords=((screen[0]/3)*1, screen[1]/2))
player2_score = entities.TextAnnouncement(player_2.points,
                                          color='red', size=75, cords=((screen[0]/3)*2, screen[1]/2))

# текст, игровое поле и звуки
pause_text = entities.TextAnnouncement(f'PAUSE',
                                       size=20)
game_over_upper_text = entities.TextAnnouncement(f'Game Over',
                                                 size=70, cords=(screen[0]/2, screen[1]/2))
game_over_lower_text = entities.TextAnnouncement(f'чтобы запустить игру нажмите цифру 2, чтобы переключить пазу - 1',
                                                 size=20, cords=(screen[0]/2, screen[1]/2+50))
help_text1 = entities.TextAnnouncement(f'Помощь:',
                                       size=16, color='gray', cords=(0, screen[1]-132))
help_text2 = entities.TextAnnouncement(f'  Движение:   player1 w & s,',
                                       size=16, color='gray', cords=(0, screen[1]-110))
help_text3 = entities.TextAnnouncement(f'              player2 up & down;',
                                       size=16, color='gray', cords=(0, screen[1]-88))
help_text4 = entities.TextAnnouncement(f'  пауза: 1,  запуск после гола - 2 (или 1);',
                                       size=16, color='gray', cords=(0, screen[1]-66))
help_text5 = entities.TextAnnouncement(f'  перезапуск сессии - Tab;',
                                       size=16, color='gray', cords=(0, screen[1]-44))
help_text6 = entities.TextAnnouncement(f'  перезапуск с сбросом очков - Back Space',
                                       size=16, color='gray', cords=(0, screen[1]-22))
midl_line = entities.Square(
    x=screen[0]/2,
    width=14,
    color=colors['LIGHT-GRAY']
)
pygame.mixer.pre_init()
pygame.mixer.music.load('ben_PGPong.mp3')
pygame.mixer.music.set_volume(5)


def restart() -> None:
    """ Перезапись всех основных переменных (restart game) """
    global start, speed, player_1, player_2, ball, player1_score, player2_score

    print(f'\nСчёт:   {player_1.points} : {player_2.points}\n\n')
    start = True
    speed = 6

    player_1 = entities.Racquet(
        screen,
        0,
        points=player_1.points
    )
    player_2 = entities.Racquet(
        screen,
        1,
        points=player_2.points
    )
    ball = entities.Ball(
        screen,
        speed,
        FPS
    )

    entities.TextAnnouncement.last_cords, entities.TextAnnouncement.last_size = ((0, 0), 0)
    player1_score.message = player_1.points
    player2_score.message = player_2.points


def events() -> None:
    """ Обработка событий.   \n

    Алгоритм работы:
     1) выход;
     2) перезапуск игры с сохранением счёта;
     3) перезапуск игры со сбросом счёта;
     4) пауза;
     5) логика движения игровых сущностей. """
    global pause, goal, speed, player_1, player_2, help_count

    # обработка событий
    for event in pygame.event.get():

        # выход из программы
        if event.type == pygame.QUIT:
            print('\n        Quit - completed')
            sys.exit()

        # если игрок нажал клавишу
        elif event.type == pygame.KEYDOWN:

            # рестарт игры без сброса очков
            if event.key == pygame.K_TAB:
                restart()
                print('\nrestart game - completed\n\n')
            # со сбросом очков
            if event.key == pygame.K_BACKSPACE:
                player_1.points, player_2.points = (0, 0)
                restart()
                print('\nset new game - completed\n\n')

            # если игрок нажал кнопку паузы
            elif (event.key == pygame.K_1) or (goal and (event.key == pygame.K_2)):
                # сейчас не паза, то поставим игру на паузу
                if not pause:
                    speed = 0
                    print('pause - on')
                # обратная ситуация
                elif pause:
                    speed = 6
                    print('pause - off')
                # каждый раз сохраняю статус игры
                pause = not pause

                # если кт-то забил гол
                if goal:
                    speed = 6
                    pause = False
                    goal = False
                    print('start game')
            elif event.key == pygame.K_3:
                help_count = not help_count

            # логика нажатия второго игрока
            if event.key == pygame.K_UP:
                player_2.m_up = True
                print('move _r player_ - up')
            elif event.key == pygame.K_DOWN:
                player_2.m_down = True
                print('move _r player_ - down')

            # логика нажатия первого игрока
            if event.key == pygame.K_w:
                player_1.m_up = True
                print('move _l player_ - up')
            elif event.key == pygame.K_s:
                player_1.m_down = True
                print('move _l player_ - down')

        # если игрок отпустил клавишу
        elif event.type == pygame.KEYUP:

            # логика отжатия второго игрока
            if event.key == pygame.K_UP:
                player_2.m_up = False
                print('move _r player_ - up')
            elif event.key == pygame.K_DOWN:
                player_2.m_down = False
                print('move _r player_ - down')

            # логика отжатия первого игрока
            if event.key == pygame.K_w:
                player_1.m_up = False
                print('move _l player_ - up')
            elif event.key == pygame.K_s:
                player_1.m_down = False
                print('move _l player_ - down')


def update_window(window) -> None:
    """ Обновление окна в каждый кадр.  \n

    Алгоритм работы:
     1) пере-заливка экрана
     2) отрисовка игрового поля
     3) добавление игровых сущностей
     4) наложение интерфейса на получившуюся картинку """

    # Заново заливаю окно цветом
    window.fill(colors['WHITE'])

    # задний фон
    midl_line.draw_rect(window)

    # игровые сущности
    if start:
        player1_score.write_text(window)
        player2_score.write_text(window)
        pygame.draw.rect(window, colors['BLACK'], (player_1.x, player_1.y, player_1.width, player_1.height))
        pygame.draw.rect(window, colors['BLACK'], (player_2.x, player_2.y, player_2.width, player_2.height))
        pygame.draw.circle(window, colors['BLACK'], (ball.x, ball.y), ball.radius)

    # 'интерфейс'
    aggregate_fps_text.write_text(window)
    if pause:
        pause_text.write_text(window)
    elif goal:
        game_over_upper_text.write_text(window, top=True)
        game_over_lower_text.write_text(window, top=True)
    if help_count:
        help_text1.write_text(window)
        help_text2.write_text(window)
        help_text3.write_text(window)
        help_text4.write_text(window)
        help_text5.write_text(window)
        help_text6.write_text(window)

    # Обновляю сам экран
    pygame.display.update()


print('\n        scripts - completed')
