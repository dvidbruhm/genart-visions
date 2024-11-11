import pygame
from pygame import gfxdraw
from utils import Vec2D, get_random_pos


class Particle:
    def __init__(
        self,
        pos: Vec2D,
        speed: float,
        size: float,
        trail_len: int,
        height: int,
        width: int,
        color: pygame.Color,
        varying_width: bool = True,
    ):
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

    def display(self, screen):
        if len(self.trail) == 0:
            return

        # pyglet.shapes.Circle(self.pos.x, self.pos.y, self.size, color=(255, 255, 255), batch=screen)
        # return

        for i, posi in enumerate(self.trail, start=1):
            p_size = (i / len(self.trail)) * self.size
            # pygame.draw.circle(screen, self.color, (posi.x, posi.y), p_size)
            gfxdraw.aacircle(screen, int(posi.x), int(posi.y), int(p_size), self.color)
            gfxdraw.filled_circle(screen, int(posi.x), int(posi.y), int(p_size), self.color)
        # pygame.draw.lines(screen, "white", False, [tuple(p) for p in self.trail])

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
