import pygame
from pygame.locals import *
from pygame.math import Vector2

from grid import Grid
import math


pygame.init()

w, h = size = 640, 480
screen = pygame.display.set_mode(size)
BLACK = Color('black')
WHITE = Color('white')
RED = Color('red')
LIGHTGRAY = Color('lightgray')

graph = pygame.Surface((w - 70, h - 70))
graph.fill(LIGHTGRAY)

angle = 45
v0_magnitude = 70
g = 9.81
p0 = Vector2(0, 0)

full_t = v0_magnitude * math.sin(math.radians(angle)) / g
l = v0_magnitude * math.cos(math.radians(angle)) * full_t

px = lambda t: p0.x + v0_magnitude * math.cos(math.radians(angle)) * t
py = lambda t: p0.y + v0_magnitude * math.sin(math.radians(angle)) * t - (g * t * t) / 2

p = Vector2()

t = 0

clock = pygame.time.Clock()

grid = Grid(graph, (50, 50))

circle = pygame.Surface((20, 20), SRCALPHA)
pygame.draw.circle(circle, RED, (10, 10), 10)

grid.add_object(0, 0, circle)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            t += 1
            p.x = px(t)
            p.y = py(t)
        grid.apply_event(event)

    screen.fill(BLACK)

    t += 0.1

    print(grid._objects[circle])
    if t != 0 and p.y < 0:
        grid._objects[circle] = (grid._objects[circle][0], -1)
        p.y = -1
    else:
        grid._objects[circle] = (px(t), py(t))
        p.x = px(t)
        p.y = py(t)

    grid.update()
    grid.render()

    pygame.draw.circle(graph, RED, (int(p.x), int(graph.get_height() - p.y)), 10)

    screen.blit(graph, (35, 35))

    pygame.display.flip()
