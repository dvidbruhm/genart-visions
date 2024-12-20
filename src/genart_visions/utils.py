import math
import random

reload = False


class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2D(self.x * other, self.y * other)
        elif isinstance(other, Vec2D):
            return Vec2D(self.x * other.x, self.y * other.y)
        raise Exception(f"Invalid type to multiply with Vec2D {type(other)}")

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vec2D(self.x / other, self.y / other)
        elif isinstance(other, Vec2D):
            return Vec2D(self.x / other.x, self.y / other.y)
        raise Exception(f"Invalid type to divide with Vec2D {type(other)}")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(%g, %g)" % (self.x, self.y)

    def __repr__(self):
        return "(%g, %g)" % (self.x, self.y)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __ne__(self, other):
        return not self.__eq__(other)

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def apply(self, func):
        "Apply a function on both the x and y component"
        return Vec2D(func(self.x), func(self.y))

    def rescale(self, magnitude: float):
        if self.mag() <= 0.01:
            return
        self.x *= magnitude / self.mag()
        self.y *= magnitude / self.mag()

    def constrain(self, magnitude: float):
        if self.mag() > magnitude:
            self.rescale(magnitude)

    @staticmethod
    def new():
        return Vec2D(0, 0)


def angle_to_vec(angle: float) -> Vec2D:
    vec = Vec2D(math.cos(angle), math.sin(angle))
    return Vec2D(vec.x / vec.mag(), vec.y / vec.mag())


def map_from_to(x, a, b, c, d):
    y = (x - a) / (b - a) * (d - c) + c
    return y


def get_random_1d_pos(start: Vec2D, end: Vec2D) -> Vec2D:
    interp = random.random()
    point = start + end * interp
    return point


def get_random_2d_pos(width: float, height: float) -> Vec2D:
    return Vec2D(random.random() * width, random.random() * height)
