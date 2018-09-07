import pygame
from pygame.locals import *
from pygame.math import Vector2
from gui import GUI, TextBox, Label, Button
from grid import Grid
from physics import Physics
import math


pygame.init()

w, h = size = 800, 600
screen = pygame.display.set_mode(size)
BLACK = Color('black')
WHITE = Color('white')
RED = Color('red')
LIGHTGRAY = Color('lightgray')
BACKGROUND = Color(192, 150, 90)

graph = pygame.Surface((w - 70, h - 70))
graph.fill(LIGHTGRAY)

gui = GUI()

gui.add_element(Label((w - 250, 48, 0, 40), 'V0 =', Color('black'), '2'))
gui.add_element(Label((w - 57, 48, 0, 40), 'м/c', Color('black'), '3'))
gui.add_element(TextBox((w - 190, 40, 130, 40), '0', name='6'))

gui.add_element(Label((w - 237, 108, 0, 40), 'α =', Color('black'), '4'))
gui.add_element(Label((w - 57, 108, 0, 40), '°', Color('black'), '5'))
gui.add_element(TextBox((w - 190, 100, 130, 40), '0', name='7'))

gui.add_element(Label((w - 247, 168, 0, 40), 'Δt =', Color('black'), '8'))
gui.add_element(Label((w - 57, 168, 0, 40), 'с', Color('black'), '9'))
gui.add_element(TextBox((w - 190, 160, 130, 40), '1', name='10'))

gui.add_element(Label((w - 247, 228, 0, 40), 'Начальная точка:', Color('black'), '12'))
gui.add_element(Label((w - 235, 268, 0, 40), 'x =', Color('black'), '13'))
gui.add_element(Label((w - 235, 308, 0, 40), 'y =', Color('black'), '14'))
gui.add_element(TextBox((w - 190, 264, 130, 35), '0', name='15'))
gui.add_element(TextBox((w - 190, 304, 130, 35), '0', name='16'))


def setup():
    if not started:
        try:
            phys.v0 = float(gui.get_element('6').text)
        except ValueError:
            phys.v0 = 0

        try:
            phys.angle = float(gui.get_element('7').text)
        except ValueError:
            phys.angle = 0

        try:
            phys.deltatime = float(gui.get_element('10').text)
        except ValueError:
            phys.deltatime = 1

        try:
            phys.p0.x = float(gui.get_element('15').text)
        except ValueError:
            phys.p0.x = 0

        try:
            phys.p0.y = float(gui.get_element('16').text)
        except ValueError:
            phys.p0.y = 0

        phys.reset()
        print('setup complete', phys)


gui.add_element(Button((w - 200, h - 60, 150, 40), 'Применить', Color('black'), func=setup, name='17'))

surf = pygame.Surface((490, h - 100))

grid = Grid(surf, (50, 50))
phys = Physics(0, 0)

grid.add_circle(phys.p0, 15, RED, 'ball')

started = False


def reset():
    global started
    started = False
    gui.del_element('11')
    gui.del_element('18')
    gui.add_element(Button((20, h - 60, 150, 40), 'Запустить', Color('black'), func=start, name='11'))
    phys.reset()
    grid.objects.clear()
    grid._original_objects.clear()
    grid._lines.clear()
    grid.add_circle(phys.p0, 15, RED, 'ball')
    print('reseted')


def pause():
    global started
    started = False
    gui.del_element('18')
    gui.add_element(Button((490 + 20 - 150, h - 60, 150, 40), 'Продолжить', Color('black'), func=resume, name='18'))


def resume():
    global started
    started = True
    gui.del_element('18')
    gui.add_element(Button((490 + 20 - 150, h - 60, 150, 40), 'Приостановить', Color('black'), func=pause, name='18'))


def start():
    global started
    started = True
    gui.del_element('11')
    gui.add_element(Button((20, h - 60, 150, 40), 'Сбросить', Color('black'), func=reset, name='11'))
    gui.add_element(Button((490 + 20 - 150, h - 60, 150, 40), 'Приостановить', Color('black'), func=pause, name='18'))
    print('started')


gui.add_element(Button((20, h - 60, 150, 40), 'Запустить', Color('black'), func=start, name='11'))

clock = pygame.time.Clock()
wait = 0

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            pass
        gui.apply_event(event)
        grid.apply_event(event)

    if started:
        if wait <= 0:
            phys.update(clock.get_fps())
            prev_point = grid.objects['ball'].point
            next_point = phys.point()
            grid.add_line(prev_point, next_point, 2, RED)

            if (next_point - prev_point).length() > 15 * 2:
                grid.add_circle(next_point, 5, RED, str(next_point))

            grid.objects['ball'].point = next_point
            wait = phys.deltatime if phys.deltatime <= 3 else 3
        else:
            wait -= 1 / clock.get_fps()

    screen.fill(BACKGROUND)

    grid.update()
    grid.render()
    # grid.draw_line(Vector2(0, 100), Vector2(100, 100))

    screen.blit(surf, (20, 20))

    gui.update()
    gui.render()

    pygame.display.flip()
