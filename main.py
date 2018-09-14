import pygame
from pygame.locals import *
from gui import GUI, TextBox, Label, Button
from grid import Grid
from physics import Physics
import logging

logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


pygame.init()

w, h = size = 800, 600
pygame.display.set_caption('Physical simulation')
screen = pygame.display.set_mode(size)
BLACK = Color('black')
WHITE = Color('white')
RED = Color('red')
BACKGROUND = Color(192, 150, 90)


gui = GUI()

gui.add_element(Label((w - 255, 40, 0, 35), 'V0=', Color('black'), 'v0_label'))
gui.add_element(Label((w - 57, 43, 0, 30), 'м/c', Color('black'), 'v0_label_units'))
gui.add_element(TextBox((w - 190, 40, 130, 35), '0.0', name='v0_textbox'))

gui.add_element(Label((w - 236, 100, 0, 35), 'α=', Color('black'), 'angle_label'))
gui.add_element(Label((w - 57, 100, 0, 35), '°', Color('black'), 'angle_label_units'))
gui.add_element(TextBox((w - 190, 100, 130, 35), '0.0', name='angle_textbox'))

gui.add_element(Label((w - 255, 160, 0, 35), 'Δt=', Color('black'), 'delta_label'))
gui.add_element(Label((w - 57, 160, 0, 35), 'с', Color('black'), 'delta_label_units'))
gui.add_element(TextBox((w - 190, 160, 130, 35), '1.0', name='delta_textbox'))

gui.add_element(Label((w - 255, 220, 0, 28), 'Начальная точка:', Color('black'), 'p0_label'))
gui.add_element(Label((w - 235, 255, 0, 35), 'x=', Color('black'), 'p0x_label'))
gui.add_element(Label((w - 235, 295, 0, 35), 'y=', Color('black'), 'p0y_label'))
gui.add_element(TextBox((w - 190, 255, 130, 35), '0.0', name='p0x_textbox'))
gui.add_element(TextBox((w - 190, 295, 130, 35), '0.0', name='p0y_textbox'))


gui.add_element(Label((w - 255, 360, 0, 28), 'Масштаб клетки:', Color('black'), 'scale_label'))
gui.add_element(Label((w - 235, 395, 0, 35), 'x=', Color('black'), 'scaleX_label'))
gui.add_element(Label((w - 235, 435, 0, 35), 'y=', Color('black'), 'scaleY_label'))
gui.add_element(TextBox((w - 190, 395, 130, 35), '50', name='scaleX_textbox'))
gui.add_element(TextBox((w - 190, 435, 130, 35), '50', name='scaleY_textbox'))


def setup():
    v0_textbox = gui.get_element('v0_textbox')
    try:
        physics.v0 = float(v0_textbox.text)
        logger.info('Для физической переменной v0 установлено значение float({})'.format(v0_textbox.text))
    except ValueError:
        if v0_textbox.text:
            logger.error('Текстовое значение v0_textbox не может быть приведено к float')
            v0_textbox.error = True

        logger.warning('Для физической переменной v0 установлено стандартное значение float({})'.format(
            v0_textbox.default_text
        ))
        physics.v0 = float(v0_textbox.default_text)

    angle_textbox = gui.get_element('angle_textbox')
    try:
        physics.angle = float(angle_textbox.text)
        logger.info('Для физической переменной angle установлено значение float({})'.format(angle_textbox.text))
    except ValueError:
        if angle_textbox.text:
            logger.error('Текстовое значение angle_textbox не может быть приведено к float')
            angle_textbox.error = True

        logger.warning('Для физической переменной angle установлено стандартное значение float({})'.format(
            angle_textbox.default_text
        ))
        physics.angle = float(angle_textbox.default_text)

    delta_textbox = gui.get_element('delta_textbox')
    try:
        physics.deltatime = float(delta_textbox.text)
        logger.info('Для физической переменной deltatime установлено значение float({})'.format(delta_textbox.text))

    except ValueError:
        if delta_textbox.text:
            logger.error('Текстовое значение delta_textbox не может быть приведено к float')
            delta_textbox.error = True

        logger.warning('Для физической переменной deltatime установлено стандартное значение float({})'.format(
            delta_textbox.default_text
        ))
        physics.deltatime = float(delta_textbox.default_text)

    p0x_textbox = gui.get_element('p0x_textbox')
    try:
        physics.p0.x = float(p0x_textbox.text)
        logger.info('Для физической переменной p0.x установлено значение float({})'.format(p0x_textbox.text))

    except ValueError:
        if p0x_textbox.text:
            logger.error('Текстовое значение p0x_textbox не может быть приведено к float')
            p0x_textbox.error = True

        logger.warning('Для физической переменной p0.x установлено стандартное значение float({})'.format(
            p0x_textbox.default_text
        ))
        physics.p0.x = float(p0x_textbox.default_text)

    p0y_textbox = gui.get_element('p0y_textbox')
    try:
        physics.p0.y = float(p0y_textbox.text)
        logger.info('Для физической переменной p0.y установлено значение float({})'.format(p0y_textbox.text))

    except ValueError:
        if p0y_textbox.text:
            logger.error('Текстовое значение p0y_textbox не может быть приведено к float')
            p0y_textbox.error = True

        logger.warning('Для физической переменной p0.y установлено стандартное значение float({})'.format(
            p0y_textbox.default_text
        ))
        physics.p0.y = float(p0y_textbox.default_text)

    scaleX_textbox = gui.get_element('scaleX_textbox')
    try:
        grid.numbers_scale = (int(scaleX_textbox.text), grid.numbers_scale[1])
        logger.info('Для переменной сетки number_scale[0] установлено значение int({})'.format(scaleX_textbox.text))

    except ValueError:
        if scaleX_textbox.text:
            logger.error('Текстовое значение scaleX_textbox не может быть приведено к int')
            scaleX_textbox.error = True

        logger.warning('Для переменной сетки number_scale[0] установлено стандартное значение int({})'.format(
            scaleX_textbox.default_text
        ))
        grid.numbers_scale = (int(scaleX_textbox.default_text), grid.numbers_scale[1])

    scaleY_textbox = gui.get_element('scaleY_textbox')
    try:
        grid.numbers_scale = (grid.numbers_scale[0], int(scaleY_textbox.text))
        logger.info('Для переменной сетки number_scale[1] установлено значение int({})'.format(scaleY_textbox.text))

    except ValueError:
        if scaleY_textbox.text:
            logger.error('Текстовое значение scaleY_textbox не может быть приведено к int')
            scaleY_textbox.error = True

        logger.warning('Для переменной сетки number_scale[1] установлено стандартное значение int({})'.format(
            scaleY_textbox.default_text
        ))
        grid.numbers_scale = (grid.numbers_scale[0], int(scaleY_textbox.default_text))

    physics.reset()
    logger.info('Настройка завершена, физические переменные: {}'.format(physics))
    reset()


gui.add_element(Button((w - 200, h - 60, 150, 40), 'Применить', Color('black'), func=setup, name='17'))

canvas = pygame.Surface((490, h - 100))

grid = Grid(canvas, (50, 50))
physics = Physics(0, 0)

grid.add_circle(physics.p0, 15, RED, 'ball')

started = False


def reset():
    global started
    started = False
    gui.del_element('reset_button')
    gui.del_element('pause_button')
    gui.del_element('resume_button')
    gui.add_element(Button((20, h - 60, 150, 40), 'Запустить', Color('black'), func=start, name='start_button'))
    physics.reset()
    grid.objects.clear()
    grid._original_objects.clear()
    grid._lines.clear()
    grid.add_circle(physics.p0, 15, RED, 'ball')
    logger.info('Симуляция сброшена')


def pause():
    global started
    started = False
    gui.del_element('pause_button')
    gui.add_element(Button(
        (490 + 20 - 200, h - 60, 200, 40), 'Продолжить',
        Color('black'), func=resume, name='resume_button'
    ))
    logger.info('Симуляция приостановлена')


def resume():
    global started
    started = True
    gui.del_element('resume_button')
    gui.add_element(Button(
        (490 + 20 - 200, h - 60, 200, 40), 'Приостановить',
        Color('black'), func=pause, name='pause_button'
    ))
    logger.info('Симуляция возобновлена')


def start():
    global started
    started = True
    gui.del_element('start_button')
    gui.add_element(Button((20, h - 60, 150, 40), 'Сбросить', Color('black'), func=reset, name='reset_button'))
    gui.add_element(Button(
        (490 + 20 - 200, h - 60, 200, 40), 'Приостановить',
        Color('black'), func=pause, name='pause_button'
    ))
    logger.info('Симуляция начата')


gui.add_element(Button((20, h - 60, 150, 40), 'Запустить', Color('black'), func=start, name='start_button'))

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
            physics.update()
            prev_point = grid.objects['ball'].point
            next_point = physics.point()
            grid.add_line(prev_point, next_point, 2, RED)

            if (next_point - prev_point).length() > 15:
                grid.add_circle(next_point, 5, RED, str(next_point))

            grid.objects['ball'].point = next_point
            wait = physics.deltatime if physics.deltatime <= 3 else 3
        else:
            wait -= 1 / clock.get_fps()

    screen.fill(BACKGROUND)

    grid.update()
    grid.render()

    screen.blit(canvas, (20, 20))

    gui.update()
    gui.render()

    pygame.display.flip()
