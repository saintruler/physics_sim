import pygame
import sys


class Grid:
    def __init__(self, surface, numbers_scale: tuple=(1, 1)):
        self.scaled = False
        self.surface = surface
        self.number_scale = numbers_scale

        self.current_x = 0 + 50
        self.current_y = 0 + self.surface.get_height() - 50

        self.cell_size = 50
        self.scale = 1
        self.xnlines = (self.surface.get_rect().width // self.cell_size) * 2
        self.ynlines = (self.surface.get_rect().height // self.cell_size) * 2

        self.font_size = 18
        self.font = pygame.font.SysFont('couriernew', self.font_size, bold=True)

        self._original_objects = {}
        self._objects = {}

    def new_hor_line(self, y_pos, width=1):
        w = pygame.display.get_surface().get_rect().width
        pygame.draw.line(self.surface, BLACK, (0, y_pos), (w, y_pos), width)

    def new_vert_line(self, x_pos, width=1):
        h = pygame.display.get_surface().get_rect().height
        pygame.draw.line(self.surface, BLACK, (x_pos, 0), (x_pos, h), width)

    def new_hor_num(self, y_pos, num):
        text = self.font.render(str(num), 3, BLACK)
        rect = text.get_rect(x=5, centery=y_pos)

        bg = pygame.Surface(rect.size)
        bg.fill(GRAY)

        self.surface.blit(bg, rect)
        self.surface.blit(text, rect)

    def new_vert_num(self, x_pos, num):
        h = self.surface.get_height()

        text = self.font.render(str(num), 3, BLACK)
        height = text.get_rect().height
        rect = text.get_rect(centerx=x_pos, y=h - height)

        bg = pygame.Surface(rect.size)
        bg.fill(GRAY)

        self.surface.blit(bg, rect)
        self.surface.blit(text, rect)

    def update(self):
        self.xnlines = (self.surface.get_rect().width // self.cell_size) * 2
        self.ynlines = (self.surface.get_rect().height // self.cell_size) * 2
        self.scaled = False

    def _scale_objects(self):
        self._objects.clear()
        for obj, point in self._original_objects.items():
            width = int(obj.get_rect().width * (1 / self.scale))
            height = int(obj.get_rect().height * (1 / self.scale))

            scaled_surf = pygame.transform.scale(obj, (width, height))

            self._objects[scaled_surf] = point

    def _render_objects(self):
        # self._scale_objects()

        for obj, point in self._objects.items():
            rect = obj.get_rect(
                centerx=self.current_x + point.x * self.cell_size / self.number_scale[0],
                centery=self.current_y - point.y * self.cell_size / self.number_scale[1]
            )
            if rect.colliderect(self.surface.get_rect()):
                self.surface.blit(obj, rect)

    def render(self):
        self.surface.fill(GRAY)

        x = self.current_x // self.cell_size
        y = self.current_y // self.cell_size

        x_pos = int(self.current_x) - x * self.cell_size + self.cell_size * 3
        self.new_vert_line(x_pos, 7)
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
            self.new_vert_num(x_pos, -(x - _) * self.number_scale[0])

        # draw numbers on horizontal lines
        for _ in range(-3, self.ynlines - 3):
            y_pos = int(self.current_y) - y * self.cell_size + self.cell_size * _
            self.new_hor_num(y_pos, (y - _) * self.number_scale[1])

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

    def add_object(self, obj: pygame.Surface, point: pygame.Vector2):
        self._original_objects[obj] = point
        self._objects = self._original_objects.copy()


BLACK = (0, 0, 0)
GRAY = (136, 136, 136)
RED = (255, 0, 0)

if __name__ == '__main__':
    pygame.init()
    w, h = size = 1280, 720
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    surf = pygame.Surface((500, 500))

    grid = Grid(surf, (40, 40))

    s = pygame.Surface((40, 40))
    s.fill(RED)
    grid.add_object(40, 40, s)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                w, h = size = event.size
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            grid.apply_event(event)

        screen.fill(GRAY)
        grid.update()
        grid.render()
        screen.blit(surf, (20, 20))
        pygame.display.flip()
