# Example file showing a basic pygame "game loop"
from p5 import *
from utils import *
import random
from perlin_noise import PerlinNoise
import math

noise2 = PerlinNoise()

def get_random_pos() -> Vec2D:
    return Vec2D(random.random() * width, random.random() * height)


class Flowfield:
    def __init__(self, resolution: int, height: int, width: int):
        self.resolution = resolution
        self.rows = math.floor(height / resolution) + 1
        self.cols = math.floor(width / resolution) + 1
        self.field = [[Vec2D.new()] * self.rows for _ in range(self.cols)]

    def create_field(self, noiseScale: float = 0.05):
        for i in range(self.cols):
            for j in range(self.rows):
                value = noise2([i * noiseScale, j * noiseScale])
                angle = map_from_to(value, 0, 1, 0, 2 * math.pi)
                self.field[i][j] = angle_to_vec(angle)

    def display(self):
        stroke(255)
        stroke_weight(2)
        fill(255)
        for i in range(self.cols):
            for j in range(self.rows):
                x = i * self.resolution
                y = j * self.resolution
                x2 = x + self.field[i][j].x * self.resolution
                y2 = y + self.field[i][j].y * self.resolution
                line(x, y, x2, y2)

    def get_value_at_pixel(self, pos: Vec2D) -> Vec2D:
        i = math.floor(pos.x / self.resolution)
        j = math.floor(pos.y / self.resolution)
        return self.field[i][j]


class Particle:
    def __init__(self, pos: Vec2D, speed: float, size: float, trail_len: int, height: int, width: int):
        self.pos = pos
        self.speed = speed
        self.size = size
        self.trail_len = trail_len
        self.trail: list[Vec2D] = []
        self.active = True
        self.height = height
        self.width = width

    def display(self):
        if len(self.trail) <= 1:
            return
        stroke(255)
        fill(255)
        circle(self.pos.x, self.pos.y, self.size)
        begin_shape(LINES)
        [vertex(p.x, p.y) for p in self.trail]
        end_shape()

    def update(self, flowfield: Flowfield):
        if not self.active:
            return
        self.add_trail()
        field_value = flowfield.get_value_at_pixel(self.pos)
        self.pos += field_value * self.speed
        self.wrap()

    def wrap(self):
        if 0 <= self.pos.x < self.width and 0 <= self.pos.y < self.height:
            return
        # self.active = False
        # return
        self.pos = get_random_pos()
        self.trail.clear()

    def add_trail(self):
        self.trail.append(self.pos)
        if len(self.trail) > self.trail_len:
            self.trail.pop(0)




flowfield: Flowfield
particles: list[Particle] = []

def setup():
    global flowfield, particles
    size(1280, 1080)
    background(0)

    flowfield = Flowfield(70, height, width)
    flowfield.create_field()

    for _ in range(10):
        particles.append(Particle(get_random_pos(), 2, 4, 10, height, width))


def draw():
    global flowfield, particles
    background(0)
    for p in particles:
        p.update(flowfield)
        p.display()

run(renderer="skia", frame_rate=60)  # "skia" is still in beta
