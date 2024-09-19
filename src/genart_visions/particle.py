from utils import Vec2D, get_random_pos
import pygame
import pygame.gfxdraw as gfxdraw

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

    def display(self, screen):
        if len(self.trail) <= 1:
            return
        # pygame.draw.circle(screen, pygame.Color(255, 255, 255), (self.pos.x, self.pos.y), self.size)
        pygame.draw.lines(screen, "white", False, [tuple(p) for p in self.trail])
        gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.size), (255, 255, 255))
        # gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.size), (255, 255, 255))

    def update(self, flowfield):
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
        self.pos = get_random_pos(self.width, self.height)
        self.trail.clear()

    def add_trail(self):
        self.trail.append(self.pos)
        if len(self.trail) > self.trail_len:
            self.trail.pop(0)
