import math
import random

# from perlin_noise import PerlinNoise
from py5 import Sketch
from utils import Vec2D, angle_to_vec, map_from_to


class Flowfield:
    def __init__(self, sketch: Sketch, resolution: int, width: int, height: int):
        self.resolution = resolution
        self.rows = math.floor(height / resolution) + 1
        self.cols = math.floor(width / resolution) + 1
        self.field = [[Vec2D.new()] * self.rows for _ in range(self.cols)]
        self.seed = random.randint(-10, 10)
        sketch.os_noise_seed(self.seed)

    def create_field(self, sketch: Sketch, noise_scale: float = 0.01):
        for i in range(self.cols):
            for j in range(self.rows):
                value = sketch.os_noise(i * noise_scale, j * noise_scale, sketch.frame_count * noise_scale * 0.02)
                angle = map_from_to(value, 0, 1, 0, 2 * math.pi)
                self.field[i][j] = angle_to_vec(angle)

    def display(self, sketch: Sketch):
        sketch.stroke(127, 127, 127, 127)
        for i in range(self.cols):
            for j in range(self.rows):
                x = i * self.resolution
                y = j * self.resolution
                x2 = x + self.field[i][j].x * self.resolution
                y2 = y + self.field[i][j].y * self.resolution
                sketch.line(x, y, x2, y2)

    def get_value_at_pixel(self, pos: Vec2D) -> Vec2D:
        i = math.floor(pos.x / self.resolution)
        j = math.floor(pos.y / self.resolution)
        return self.field[i][j]
