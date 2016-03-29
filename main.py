import pygame
from robot import Robot
from figure import Figure
from settings_storage import settings


if __name__ == '__main__':
    settings.load('settings')

    pygame.init()
    gameDisplay = pygame.display.set_mode(settings.DISPLAY_RES)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 25)
    text = pygame.font.SysFont("monospace", 15)

    figures = [Figure(pygame) for i in range(settings.FIGURES_COUNT)]

    robot = Robot(pygame, gameDisplay, settings.SPAWN_POINT, 0)

    delta_alpha = 0
    stop = False
    while not stop:
        # EVENTS #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop = True

                if event.key == pygame.K_DOWN:
                    delta_alpha += 0.001
                if event.key == pygame.K_UP:
                    delta_alpha -= 0.001

                if event.key == pygame.K_w:
                    robot.move(0, -5)
                if event.key == pygame.K_s:
                    robot.move(0, 5)
                if event.key == pygame.K_a:
                    robot.move(-5, 0)
                if event.key == pygame.K_d:
                    robot.move(5, 0)

        # DRAW #
        gameDisplay.fill(settings.white)

        label = text.render('da: ' + str(round(delta_alpha, 4)), 1, settings.black)
        gameDisplay.blit(label, (10, 10))

        robot.draw_vision(gameDisplay, figures)

        for figure in figures:
            figure.draw(gameDisplay)

        # UPDATE #

        pygame.display.update()
        clock.tick(settings.FPS)
        robot.update(delta_alpha)
        pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))

    pygame.quit()
