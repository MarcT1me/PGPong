import pygame

import scripts
print('\n        main imports  - completed\n\n')


def main() -> None:
    """ Главная функция программы (restart - False) """

    # работа программы
    running: bool = True

    # Работа с PyGame
    clock = scripts.clock
    FPS = scripts.FPS
    screen = scripts.screen
    window = pygame.display.set_mode(screen)
    pygame.display.set_caption("Pong Game       v1")

    print('\nstart application - completed\n')

    while running:
        """ Главны цикл игры"""

        # ограничение на кол-во обновлений экрана в секунду
        clock.tick(FPS)
        scripts.aggregate_fps_count = int(clock.get_fps())
        scripts.aggregate_fps_text.message = f'FPS: {scripts.aggregate_fps_count}'

        # обработка событий
        scripts.events()
        speed = scripts.speed

        # обновление сущностей
        scripts.player_1.update_racquet(screen, FPS, speed)
        scripts.player_2.update_racquet(screen, FPS, speed)
        if not scripts.pause and not scripts.goal:
            scripts.ball.update_ball(screen, scripts.player_1, scripts.player_2)

        # обновление окна игры
        scripts.update_window(window)

    if scripts.start == 'restart':
        print('restart application - process\n')
        main()


if __name__ == '__main__':
    main()
# на всякий случай закрываю окно
pygame.quit()
print('\n        Quit - completed')
