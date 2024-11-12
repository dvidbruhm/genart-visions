import os

from py5 import Sketch
from utils import Vec2D, get_random_pos

os.environ["JAVA_HOME"] = "C:\Program Files\Microsoft\jdk-21.0.5.11-hotspot"


class Particle:
    def __init__(self, pos: Vec2D, speed: float, size: float, trail_len: int, height: int, width: int, color, varying_width: bool = True):
        self.pos = pos
        self.speed = speed
        self.size = size
        self.trail_len = trail_len
        self.trail: list[Vec2D] = []
        self.active = True
        self.height = height
        self.width = width
        self.color = color
        self.varying_width = varying_width
        self.add_trail()

    def display(self, sketch: Sketch):
        if len(self.trail) <= 1:
            return

        sketch.fill(255, 255, 255)
        sketch.stroke(255, 255, 255)
        size = self.size
        for i in range(len(self.trail) - 1):
            current_pos, next_pos = self.trail[i], self.trail[i + 1]
            if self.varying_width:
                size = ((i + 1) / len(self.trail)) * self.size
            # sketch.circle(posi.x, posi.y, size)
            sketch.stroke_weight(size)
            sketch.line(current_pos.x, current_pos.y, next_pos.x, next_pos.y)

    def update(self, flowfield):
        if not self.active:
            return
        field_value = flowfield.get_value_at_pixel(self.pos)
        self.pos += field_value * self.speed
        self.wrap()
        self.add_trail()

    def wrap(self):
        if 0 <= self.pos.x < self.width and 0 <= self.pos.y < self.height:
            return
        # self.active = False
        # return
        self.pos = get_random_pos(self.width, self.height)
        self.trail.clear()

    def add_trail(self):
        self.trail.append(self.pos)
        if len(self.trail) > self.trail_len:
            self.trail.pop(0)
