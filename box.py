import pygame
from pygame.locals import *

class Box:
    def __init__(self, bbox:Rect, radius, margin=4):
        self.bbox = bbox
        self.radius = radius
        self.margin = margin

    def draw_background(self, surface):
        pygame.draw.circle(surface, BLACK, (self.radius, self.radius), self.radius)
        pygame.draw.circle(surface, BLACK, (surface.get_width() - self.radius, self.radius), self.radius)
        pygame.draw.circle(surface, BLACK, (self.radius, surface.get_height() - self.radius), self.radius)
        pygame.draw.circle(surface, BLACK, (surface.get_width() - self.radius, surface.get_height() - self.radius), self.radius)
        pygame.draw.rect(surface, BLACK, (0, self.radius, surface.get_width(), surface.get_height() - self.radius * 2))
        pygame.draw.rect(surface, BLACK, (self.radius, 0, surface.get_width() - self.radius * 2, surface.get_height()))

    def draw_foreground(self, surface):
        pygame.draw.circle(surface, WHITE, (
            self.radius + self.margin, self.radius + self.margin
        ), self.radius)

        pygame.draw.circle(surface, WHITE, (
            surface.get_width() - self.radius - self.margin,
            self.radius + self.margin
        ), self.radius)

        pygame.draw.circle(surface, WHITE, (
            self.radius + self.margin, surface.get_height() - self.radius - self.margin
        ), self.radius)

        pygame.draw.circle(surface, WHITE, (
            surface.get_width() - self.radius - self.margin,
            surface.get_height() - self.radius - self.margin
        ), self.radius)

        pygame.draw.rect(surface, WHITE, (
            self.margin, self.radius + self.margin,
            surface.get_width() - self.margin * 2, surface.get_height() - self.radius * 2 - self.margin * 2
        ))

        pygame.draw.rect(surface, WHITE, (
            self.radius + self.margin, self.margin,
            surface.get_width() - self.radius * 2 - self.margin * 2, surface.get_height() - self.margin * 2
        ))

    def draw(self, surface):
        base = pygame.Surface(self.bbox.size, SRCALPHA)
        self.draw_background(base)
        self.draw_foreground(base)

        surface.blit(base, self.bbox)

pygame.init()

w, h = size = 640, 480
screen = pygame.display.set_mode(size)
BLACK = Color('black')
WHITE = Color('white')
RED = Color('red')
LIGHTGRAY = Color('lightgray')

graph = pygame.Surface((w - 70, h - 70))
graph.fill(LIGHTGRAY)

b = Box(Rect(20, 10, 50, 20), 9, 2)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            b.radius = 10

    screen.fill(BLACK)

    b.draw(graph)

    screen.blit(graph, (35, 35))

    pygame.display.flip()
