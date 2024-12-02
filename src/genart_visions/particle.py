import os

import utils
from py5 import Sketch
from typing_extensions import Self

os.environ["JAVA_HOME"] = "C:\Program Files\Microsoft\jdk-21.0.5.11-hotspot"


class Particle:
    def __init__(
        self,
        pos: utils.Vec2D,
        max_speed: float,
        size: float,
        trail_len: int,
        height: int,
        width: int,
        color,
        wrap: bool = True,
        varying_width: bool = False,
        acceleration: float | None = None,
        friction: float = 0.97,
    ):
        self.pos = pos
        self.max_speed = max_speed
        self.velocity = utils.Vec2D(0, 0)
        self.size = size
        self.trail_len = trail_len
        self.trail: list[utils.Vec2D] = []
        self.active = True
        self.height = height
        self.width = width
        self.color = color
        self.wrap = wrap
        self.varying_width = varying_width
        self.add_trail()
        self.acceleration = acceleration
        self.friction = friction

    def display(self, sketch: Sketch):
        sketch.fill(self.color)
        sketch.no_fill()
        sketch.stroke(self.color)

        if len(self.trail) <= 1:
            sketch.stroke_weight(self.size)
            # sketch.no_fill()
            sketch.point(self.pos.x, self.pos.y)
            return

        if self.varying_width:
            # TODO
            for i in range(len(self.trail) - 1):
                current_pos = self.trail[i]
                next_pos = self.trail[i + 1]
                if self.varying_width:
                    self.size = ((i + 1) / len(self.trail)) * self.size
                sketch.stroke_weight(self.size)
                sketch.point(current_pos.x, current_pos.y)
                # sketch.circle(current_pos.x, current_pos.y, size)
                # sketch.line(current_pos.x, current_pos.y, next_pos.x, next_pos.y)
        else:
            sketch.stroke_weight(self.size)
            sketch.begin_shape()
            for i in range(len(self.trail)):
                sketch.curve_vertex(self.trail[i].x, self.trail[i].y)
            sketch.end_shape()

    def update(self, flowfield):
        if not self.active:
            return

        field_value = flowfield.get_value_at_pixel(self.pos)

        if self.acceleration:
            self.velocity += field_value * self.acceleration
            # self.velocity.constrain(self.max_speed)
            self.pos += self.velocity
            self.velocity *= self.friction
        else:
            self.pos += field_value * self.max_speed

        if self.wrap:
            if not self.is_inbounds():
                self.reset_pos()
        self.add_trail()

    def is_inbounds(self):
        if 0 <= self.pos.x < self.width and 0 <= self.pos.y < self.height:
            return True
        return False

    def reset_pos(self):
        self.active = False
        return
        self.pos = utils.get_random_2d_pos(self.width, self.height)
        # self.pos = utils.get_random_1d_pos(utils.Vec2D(0, 0), utils.Vec2D(self.width, self.height))
        self.trail.clear()
        self.velocity = utils.Vec2D(0, 0)

    def add_trail(self):
        self.trail.append(self.pos)
        if len(self.trail) > self.trail_len:
            self.trail.pop(0)

    def collision(self, other: Self, other_pos: utils.Vec2D):
        dist = self.pos.dist(other_pos)
        if dist < (self.size + other.size) / 2 + 1:
            self.reset_pos()

    def collision_all(self, others: list[Self]):
        for other in others:
            if self == other or not self.active:
                continue
            for pos in other.trail:
                self.collision(other, pos)
