import pygame
from pygame import Color


def load_image(path):
    return pygame.image.load(path).convert_alpha()


class Label:
    def __init__(self, rect, text, font_color, name):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font_color = font_color
        self.name = name

        self.font = pygame.font.Font(None, self.rect.h - 4)

    def render(self, surface):
        rendered_text = self.font.render(self.text, 1, self.font_color)
        surface.blit(rendered_text, self.rect.topleft)


class TextBox:
    def __init__(self, rect, default_text='', callback=None, name=''):
        self.active = False
        self.blink = True
        self.blink_timer = 0
        self.caret = 0

        self.rect = pygame.Rect(rect)

        self.flag_first_active = True
        self.default_text = default_text

        self.text = ''
        self.font = pygame.font.SysFont('couriernew', self.rect.height - 15, bold=True)
        self.font_color = Color('Black')

        self.name = name
        self.callback = callback
        self.error = False

    def apply_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                if callable(self.callback):
                    self.callback(self.text)
                    self.text = ''
                    self.caret = 0

            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0 and self.caret != 0:
                    self.text = self.text[:self.caret - 1] + self.text[self.caret:]
                    if self.caret > 0:
                        self.caret -= 1

            elif event.key == pygame.K_LEFT:
                if self.caret > 0:
                    self.caret -= 1

            elif event.key == pygame.K_RIGHT:
                if self.caret < len(self.text):
                    self.caret += 1

            else:
                if self.font.render(self.text + event.unicode, 1, self.font_color).get_rect().w < self.rect.w:
                    self.text = self.text[:self.caret] + event.unicode + self.text[self.caret:]
                    self.caret += 1

            self.error = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active = self.rect.collidepoint(event.pos)
                if self.active:
                    if len(self.text) > 0 and self.text != self.default_text:
                        self.caret = (event.pos[0] - self.rect.x) // (self.rendered_rect.width // len(self.text))
                        if self.caret >= len(self.text):
                            self.caret = len(self.text)
                    else:
                        self.caret = 0

    def update(self):
        if self.active and self.flag_first_active:
            self.flag_first_active = False
            self.text = ''
            self.caret = 0

        elif not self.active and not self.flag_first_active and self.text == '':
            self.flag_first_active = True
            self.caret = 0

        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render_frame(self, surface):
        color = Color('black')
        pygame.draw.line(
            surface, color, (0, 0),
            (0, self.rect.h), 2
        )
        pygame.draw.line(
            surface, color, (0, self.rect.h - 2),
            (self.rect.w, self.rect.h - 2), 2
        )
        pygame.draw.line(
            surface, color, (self.rect.w - 2, 0),
            (self.rect.w - 2, self.rect.h), 2
        )
        pygame.draw.line(
            surface, color, (0, 0),
            (self.rect.w, 0), 2
        )

    def render_text(self, surface):
        if self.text:
            color = self.font_color
        elif self.error:
            color = self.font_color
        else:
            color = Color('gray')
        text = self.text if self.text or self.active else self.default_text
        self.rendered_text = self.font.render(text, 1, color)
        self.rendered_rect = self.rendered_text.get_rect(x=4, centery=self.rect.h // 2)
        surface.blit(self.rendered_text, self.rendered_rect)

    def render(self, surface):
        surf = pygame.Surface(self.rect.size)
        if self.error:
            surf.fill(Color('#FF7167'))
        else:
            surf.fill(Color('white'))

        self.render_frame(surf)
        self.render_text(surf)

        if self.blink and self.active:
            w = self.font.render(self.text[:self.caret], 1, self.font_color).get_width()
            pygame.draw.line(
                surf, pygame.Color("black"),
                (w + 2, self.rendered_rect.top + 2),
                (w + 2, self.rendered_rect.bottom - 2)
            )

        surface.blit(surf, self.rect)


class Checkbox:
    def __init__(self, name, rect: pygame.Rect, value=False, func=(lambda val, *args: None), *args):
        self.name = name
        self.args = args

        self.rect = rect

        self.func = func
        self.value = value

        self.states = {
            'hovered': False,
            'clicked': False
        }

        self.images = {
            'normal': {
                True: self.normal_checked(),
                False: self.normal_unchecked()
            },
            'hovered': {
                True: self.hovered_checked(),
                False: self.hovered_unchecked()
            }
        }

        self.image = self.images['normal'][value]

    def normal_unchecked(self):
        surf = pygame.Surface(self.rect.size)
        surf.fill(Color('white'))
        pygame.draw.rect(surf, Color('black'), (0, 0, *self.rect.size), 3)
        return surf

    def normal_checked(self):
        surf = self.normal_unchecked()
        pygame.draw.line(surf, Color('black'), (0, 0), self.rect.size, 3)
        pygame.draw.line(surf, Color('black'), (0, self.rect.height), (self.rect.width, 0), 3)
        return surf

    def hovered_unchecked(self):
        surf = pygame.Surface(self.rect.size)
        surf.fill(Color('lightgray'))
        pygame.draw.rect(surf, Color('black'), (0, 0, *self.rect.size), 3)
        return surf

    def hovered_checked(self):
        surf = self.hovered_unchecked()
        pygame.draw.line(surf, Color('black'), (0, 0), self.rect.size, 3)
        pygame.draw.line(surf, Color('black'), (0, self.rect.height), (self.rect.width, 0), 3)
        return surf

    def update(self):
        if self.states['hovered']:
            self.image = self.images['hovered'][self.value]
        else:
            self.image = self.images['normal'][self.value]

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def apply_event(self, event):
        self.states['hovered'] = self.rect.collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.states['hovered'] and self.states['clicked']:
                    self.value = not self.value
                    self.states['clicked'] = False
                    self.func(self.value, *self.args)


class CheckboxWithText(Checkbox):
    def __init__(self, name, pos, image_states, text, font_path, text_color, text_size,
                 value=False, func=lambda val, *args: None, *args):
        super().__init__(name, pos, image_states, value, func, *args)
        self.font = pygame.font.Font(font_path, text_size)
        self.text_color = pygame.Color(text_color)
        self.text = text

        self.text_surf = self.font.render(self.text, 1, self.text_color)
        self.rect = pygame.Rect(0, 0,
                                self.text_surf.get_width() + self.image.get_width(),
                                self.text_surf.get_height(),
                                )
        self.rect.center = self.pos

    def update(self):
        super().update()
        self.text_surf = self.font.render(self.text, 1, self.text_color)
        self.rect = pygame.Rect(0, 0,
                                self.text_surf.get_width() + self.image.get_width(),
                                self.text_surf.get_height(),
                                )
        self.rect.center = self.pos

    def render(self, surface):
        surface.blit(self.text_surf, self.text_surf.get_rect(left=self.rect.left, centery=self.pos[1]))
        surface.blit(self.image, self.image.get_rect(right=self.rect.right, centery=self.pos[1]))


class Button:
    def __init__(self, rect, text, text_color, text_size=None, name='',
                 func=(lambda *args: None), *args):

        self.rect = pygame.Rect(rect)
        self.normal_image = self.normal()
        self.hover_image = self.hovered()
        self.click_image = self.clicked()

        self.text = text
        self.font = pygame.font.SysFont('couriernew', text_size if text_size is not None else self.rect.h - 15, bold=True)
        self.text_color = text_color

        self.image = self.normal_image

        self.name = name
        self.func = func
        self.args = args

        self.states = {
            'hovered': False,
            'clicked': False,
            'after_click': False
        }

    def normal(self):
        surf = pygame.Surface(self.rect.size)
        surf.fill(Color('white'))
        pygame.draw.rect(surf, Color('black'), (0, 0, *self.rect.size), 3)
        return surf

    def hovered(self):
        surf = pygame.Surface(self.rect.size)
        surf.fill(Color('gray'))
        pygame.draw.rect(surf, Color('black'), (0, 0, *self.rect.size), 3)
        return surf

    def clicked(self):
        surf = pygame.Surface(self.rect.size)
        surf.fill(Color('darkgray'))
        pygame.draw.rect(surf, Color('black'), (0, 0, *self.rect.size), 3)
        return surf

    def update(self):
        if self.states['clicked']:
            self.states['clicked'] = False
            self.image = self.click_image
            self.states['after_click'] = True

        elif self.states['after_click']:
            if self.states['hovered']:
                self.image = self.click_image
            else:
                self.states['after_click'] = False

        elif self.states['hovered']:
            self.image = self.hover_image

        else:
            self.image = self.normal_image

    def render(self, surface):
        surface.blit(self.image, self.rect)
        text = self.font.render(self.text, 4, self.text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def apply_event(self, event):
        self.states['hovered'] = self.rect.collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.states['hovered'] and self.states['after_click']:
                    self.states['after_click'] = False
                    self.func(*self.args)


class GUI:
    elements = []

    @staticmethod
    def add_element(element):
        if all(map(lambda elem: elem.name != element.name, GUI.elements)):
            GUI.elements.append(element)
            return element

    @staticmethod
    def get_element(name):
        for elem in GUI.elements:
            if elem.name == name:
                return elem

    @staticmethod
    def render():
        for element in GUI.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(pygame.display.get_surface())

    @staticmethod
    def update():
        for element in GUI.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    @staticmethod
    def apply_event(event):
        for element in GUI.elements:
            get_event = getattr(element, "apply_event", None)
            if callable(get_event):
                element.apply_event(event)

    @staticmethod
    def del_element(*names):
        for element in GUI.elements.copy():
            if element.name in names:
                GUI.elements.remove(element)

    @staticmethod
    def clear():
        GUI.elements = []
