import pygame
from pygame.locals import *
from gui import GUI, TextBox, Label, Button
from grid import Grid
from physics import Physics


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
gui.add_element(TextBox((w - 190, 40, 130, 40), 'Скорость', name='6'))

gui.add_element(Label((w - 237, 108, 0, 40), 'α =', Color('black'), '4'))
gui.add_element(Label((w - 57, 108, 0, 40), '°', Color('black'), '5'))
gui.add_element(TextBox((w - 190, 100, 130, 40), 'Угол', name='7'))

gui.add_element(Label((w - 247, 168, 0, 40), 'Δt =', Color('black'), '8'))
gui.add_element(Label((w - 57, 168, 0, 40), 'с', Color('black'), '9'))
gui.add_element(TextBox((w - 190, 160, 130, 40), 'Интервал', name='10'))

gui.add_element(Label((w - 247, 228, 0, 40), 'Начальная точка:', Color('black'), '12'))
gui.add_element(Label((w - 235, 268, 0, 40), 'x =', Color('black'), '13'))
gui.add_element(Label((w - 235, 308, 0, 40), 'y =', Color('black'), '14'))
gui.add_element(TextBox((w - 190, 264, 130, 35), 'Число', name='15'))
gui.add_element(TextBox((w - 190, 304, 130, 35), 'Число', name='16'))

def setup():
    if not started:
        phys.v0 = float(gui.get_element('6').text)
        phys.angle = float(gui.get_element('7').text)
        phys.deltatime = float(gui.get_element('10').text)
        phys.p0 = pygame.Vector2(float(gui.get_element('15').text), float(gui.get_element('16').text))
        phys.reset()
        print('setup complete')



gui.add_element(Button((w - 200, h - 60, 150, 40), 'Применить', Color('black'), func=setup, name='17'))

surf = pygame.Surface((490, h - 100))

grid = Grid(surf, (50, 50))
phys = Physics(0, 0)

ball = pygame.Surface((30, 30), SRCALPHA)
pygame.draw.circle(ball, RED, (15, 15), 15)

grid.add_object(ball, phys.p0)

started = False


def start():
    global started
    started = True
    print('started')


gui.add_element(Button((20, h - 60, 150, 40), 'Запустить', Color('black'), func=start, name='11'))

clock = pygame.time.Clock()

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
        phys.update()
        grid._objects[ball] = phys.point()
        print('updated', phys.t)
    else:
        grid._objects[ball] = phys.p0

    screen.fill(BACKGROUND)

    grid.update()
    grid.render()

    screen.blit(surf, (20, 20))

    gui.update()
    gui.render()

    pygame.display.flip()
