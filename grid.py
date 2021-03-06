import pygame
from pygame.locals import *


class GridObject:
    def __init__(self, surface: pygame.Surface, point: pygame.Vector2):
        self.surface = surface
        self.point = point


class Grid:
    def __init__(self, surface, numbers_scale: tuple=(1, 1), lines_color=Color('black'), background_color=(136, 136, 136)):
        self.scaled = False
        self.surface = surface
        self.numbers_scale = (abs(numbers_scale[0]), abs(numbers_scale[1]))

        self.current_x = self.numbers_scale[0]
        self.current_y = self.surface.get_height() - self.numbers_scale[1]

        self.cell_size = 50
        self.scale = 1
        self.xnlines = (self.surface.get_rect().width // self.cell_size) * 2
        self.ynlines = (self.surface.get_rect().height // self.cell_size) * 2

        self.font_size = 18
        self.font = pygame.font.SysFont('couriernew', self.font_size, bold=True)
        
        self.lines_color = lines_color
        self.background_color = background_color

        self._original_objects = {}
        self.objects = {}
        self._lines = []

    def new_hor_line(self, y_pos, width=1):
        w = pygame.display.get_surface().get_rect().width
        pygame.draw.line(self.surface, self.lines_color, (0, y_pos), (w, y_pos), width)

    def new_vert_line(self, x_pos, width=1):
        h = pygame.display.get_surface().get_rect().height
        pygame.draw.line(self.surface, self.lines_color, (x_pos, 0), (x_pos, h), width)

    def new_hor_num(self, y_pos, num):
        text = self.font.render(str(num), 3, self.lines_color)
        rect = text.get_rect(x=5, centery=y_pos)

        bg = pygame.Surface(rect.size)
        bg.fill(self.background_color)

        self.surface.blit(bg, rect)
        self.surface.blit(text, rect)

    def new_vert_num(self, x_pos, num):
        h = self.surface.get_height()

        text = self.font.render(str(num), 3, self.lines_color)
        height = text.get_rect().height
        rect = text.get_rect(centerx=x_pos, y=h - height)

        bg = pygame.Surface(rect.size)
        bg.fill(self.background_color)

        self.surface.blit(bg, rect)
        self.surface.blit(text, rect)

    def update(self):
        self.xnlines = (self.surface.get_rect().width // self.cell_size) * 2
        self.ynlines = (self.surface.get_rect().height // self.cell_size) * 2
        self.scaled = False

    def _scale_objects(self):
        self.objects.clear()
        for name, obj in self._original_objects.items():
            width = int(obj.surface.get_rect().width * (1 / self.scale))
            height = int(obj.surface.get_rect().height * (1 / self.scale))

            scaled_surf = pygame.transform.scale(obj.surface, (width, height))

            self.objects[name] = GridObject(scaled_surf, obj.point)

    def _render_objects(self):
        # self._scale_objects()

        for obj in self.objects.values():
            rect = obj.surface.get_rect(
                centerx=self.current_x + obj.point.x * self.cell_size / self.numbers_scale[0],
                centery=self.current_y - obj.point.y * self.cell_size / self.numbers_scale[1]
            )
            if rect.colliderect(self.surface.get_rect()):
                self.surface.blit(obj.surface, rect)

    def draw_line(self, p0: pygame.Vector2, p1: pygame.Vector2, w: float, color: pygame.Color):
        pygame.draw.line(
            self.surface, color,
            (
                self.current_x + p0.x * self.cell_size / self.numbers_scale[0],
                self.current_y - p0.y * self.cell_size / self.numbers_scale[1]
            ),
            (
                self.current_x + p1.x * self.cell_size / self.numbers_scale[0],
                self.current_y - p1.y * self.cell_size / self.numbers_scale[1]
            ), w
        )

    def render(self):
        self.surface.fill(self.background_color)

        x = self.current_x // self.cell_size
        y = self.current_y // self.cell_size

        for p0, p1, w, color in self._lines:
            self.draw_line(p0, p1, w, color)

        # draw vertical lines
        for _ in range(-3, self.xnlines - 3):
            x_pos = int(self.current_x) - x * self.cell_size + self.cell_size * _
            width = 5 if x - _ == 0 else 1
            self.new_vert_line(x_pos, width)

        # draw horizontal lines
        for _ in range(self.ynlines):
            y_pos = int(self.current_y) - y * self.cell_size + self.cell_size * _
            width = 5 if y - _ == 0 else 1
            self.new_hor_line(y_pos, width)

        self._render_objects()

        # draw numbers on vertical lines
        for _ in range(-3, self.xnlines - 3):
            x_pos = int(self.current_x) - x * self.cell_size + self.cell_size * _
            self.new_vert_num(x_pos, -(x - _) * self.numbers_scale[0])

        # draw numbers on horizontal lines
        for _ in range(-3, self.ynlines - 3):
            y_pos = int(self.current_y) - y * self.cell_size + self.cell_size * _
            self.new_hor_num(y_pos, (y - _) * self.numbers_scale[1])

    def resize(self, delta):
        if delta < 0:
            # scale up
            if self.cell_size + 10 < 150:
                self.font_size += 2
                self.font = pygame.font.SysFont('couriernew', self.font_size, bold=True)

                self.cell_size += 10
                self.scale = 50 / self.cell_size

                if self.font_size < 18:
                    self.xnlines -= 15
                    self.ynlines -= 15
        else:
            # scale down
            if self.cell_size - 10 > 20:
                self.font_size -= 2
                self.font = pygame.font.SysFont('couriernew', self.font_size, bold=True)

                self.cell_size -= 10
                self.scale = 50 / self.cell_size

                self.xnlines += 15
                self.ynlines += 15

    def move(self, delta_x, delta_y):
        self.current_x += delta_x
        self.current_y += delta_y

    def apply_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5) and not self.scaled:
                self.resize(event.button - 5)

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            self.move(*event.rel)

        elif event.type == pygame.VIDEORESIZE:
            self.scaled = True

    def add_object(self, obj: pygame.Surface, point: pygame.Vector2, name: str):
        self._original_objects[name] = GridObject(obj, point)
        self.objects = self._original_objects.copy()

    def add_line(self, p0: pygame.Vector2, p1: pygame.Vector2, w: float, color: pygame.Color):
        self._lines.append((p0, p1, w, color))

    def add_circle(self, point: pygame.Vector2, radius: float, color: pygame.Color, name: str):
        circle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle, color, (radius, radius), radius)
        self.add_object(circle, point, name)
