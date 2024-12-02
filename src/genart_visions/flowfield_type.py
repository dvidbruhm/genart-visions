import math
import random
from dataclasses import dataclass

from py5 import Py5Image
from utils import Vec2D, angle_to_vec, map_from_to


class FieldType:
    def get_value_at_pixel(self, pos: Vec2D, ff) -> Vec2D:
        raise NotImplementedError()


@dataclass
class Noise(FieldType):
    noise_scale: float = 0.1

    def get_value_at_pixel(self, pos: Vec2D, ff) -> Vec2D:
        value = ff.sketch.os_noise(pos.x * self.noise_scale, pos.y * self.noise_scale, ff.sketch.frame_count * self.noise_scale * 0.02)
        angle = map_from_to(value, 0, 1, 0, 2 * math.pi)
        return angle_to_vec(angle)


@dataclass
class Clifford(FieldType):
    a: float = random.uniform(-2.0, 2.0)
    b: float = random.uniform(-2.0, 2.0)
    c: float = random.uniform(-2.0, 2.0)
    d: float = random.uniform(-2.0, 2.0)

    def get_value_at_pixel(self, pos: Vec2D, ff) -> Vec2D:
        # i = math.floor(pos.x)
        # j = math.floor(pos.y)
        scale = 0.005
        x = (pos.x - ff.width / 2) * scale
        y = (pos.y - ff.height / 2) * scale
        x1 = math.sin(self.a * y) + self.c * math.cos(self.a * x)
        y1 = math.sin(self.b * x) + self.d * math.cos(self.b * y)
        angle = math.atan2(y1 - y, x1 - x)
        return angle_to_vec(angle)


@dataclass
class SinCos(FieldType):
    scale: float = 0.002


@dataclass
class FromImage(FieldType):
    def setup(self, image: Py5Image):
        self.image = image
        self.image.load_pixels()

    def get_value_at_pixel(self, pos: Vec2D, ff) -> Vec2D:
        c = self.image.pixels[int(pos.x) + self.image.width * int(pos.y)]
        value = ff.sketch.brightness(ff.sketch.color(c))
        angle = map_from_to(value, 0, 255, 0, 2 * math.pi)
        return angle_to_vec(angle)
