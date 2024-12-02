import math

from flowfield_type import FieldType

# from perlin_noise import PerlinNoise
from py5 import Sketch
from utils import Vec2D


class Flowfield:
    def __init__(self, sketch: Sketch, resolution: int, width: int, height: int, field_type: FieldType):
        self.resolution = resolution
        self.rows = math.floor(height / resolution) + 1
        self.cols = math.floor(width / resolution) + 1
        self.field = [[Vec2D.new()] * self.rows for _ in range(self.cols)]
        self.width = sketch.width
        self.height = sketch.height
        self.field_type = field_type
        self.sketch = sketch

    def display(self):
        self.sketch.stroke(127, 127, 127, 127)
        self.sketch.stroke_weight(1)

        for i in range(self.cols):
            for j in range(self.rows):
                pos = Vec2D(i, j) * self.resolution - Vec2D(1, 1)
                value = self.field_type.get_value_at_pixel(pos, self)
                pos2 = pos + (value * self.resolution)
                self.sketch.stroke_weight(1)
                self.sketch.line(pos.x, pos.y, pos2.x, pos2.y)
                self.sketch.stroke_weight(3)
                self.sketch.point(pos2.x, pos2.y)

    def get_value_at_pixel(self, pos: Vec2D) -> Vec2D:
        return self.field_type.get_value_at_pixel(pos, self)
