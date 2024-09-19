import math
import pygame
from perlin_noise import PerlinNoise
from utils import Vec2D, angle_to_vec, map_from_to


class Flowfield:
    def __init__(self, resolution: int, height: int, width: int):
        self.resolution = resolution
        self.rows = math.floor(height / resolution) + 1
        self.cols = math.floor(width / resolution) + 1
        self.field = [[Vec2D.new()] * self.rows for _ in range(self.cols)]
        self.noise = PerlinNoise()

    def create_field(self, noiseScale: float = 0.01):
        for i in range(self.cols):
            for j in range(self.rows):
                value = self.noise([i * noiseScale, j * noiseScale])
                angle = map_from_to(value, 0, 1, 0, 2 * math.pi)
                self.field[i][j] = angle_to_vec(angle)

    def display(self, screen):
        for i in range(self.cols):
            for j in range(self.rows):
                x = i * self.resolution
                y = j * self.resolution
                x2 = x + self.field[i][j].x * self.resolution
                y2 = y + self.field[i][j].y * self.resolution
                pygame.draw.line(screen, 255, (x, y), (x2, y2))

    def get_value_at_pixel(self, pos: Vec2D) -> Vec2D:
        i = math.floor(pos.x / self.resolution)
        j = math.floor(pos.y / self.resolution)
        return self.field[i][j]
