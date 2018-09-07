from pygame.math import Vector2
from math import cos, sin, radians

class Physics:
    def __init__(self, angle: float, v0: float, deltatime: float=1, g: float=9.81, p0: Vector2=Vector2()):
        self.angle = angle
        self.v0 = v0
        self.g = g
        self.p0 = p0

        self.t = 0
        self.deltatime = deltatime

    def px(self):
        return self.p0.x + self.v0 * cos(radians(self.angle)) * self.t

    def py(self):
        return self.p0.y + self.v0 * sin(radians(self.angle)) * self.t - (self.g * self.t ** 2) / 2

    def point(self):
        return Vector2(self.px(), self.py())

    def set_t(self, t: float):
        self.t = t

    def set_deltatime(self, deltatime: float):
        self.deltatime = deltatime

    def set_angle(self, angle: float):
        self.angle = angle

    def set_v0(self, v0: float):
        self.v0 = v0

    def set_p0(self, p0: Vector2):
        self.p0 = p0

    def update(self):
        self.t += self.deltatime

    def reset(self):
        self.t = 0
