import math
from typing import Sequence

from py5 import Sketch
from utils import Vec2D


def sand_line(sketch: Sketch):
    pass


def rect_points(x: float, y: float, width: float, height: float, n_points_per_side: int):
    points = []
    cur_x, cur_y = x, y
    inc_x, inc_y = width / n_points_per_side, height / n_points_per_side
    for dir_x, dir_y in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
        for i in range(n_points_per_side):
            points.append(Vec2D(cur_x, cur_y))
            cur_x += inc_x * dir_x
            cur_y += inc_y * dir_y
    points.reverse()
    points.insert(0, points.pop())
    return points


def circle_points(x: float, y: float, r: float, n_points: int) -> Sequence[Vec2D]:
    angles = [(i * 2 * math.pi) / n_points for i in range(n_points)]
    points = [Vec2D(r * math.cos(angle) + x, r * math.sin(angle) + y) for angle in angles]
    points.reverse()
    points.insert(0, points.pop())
    return points


def extrude_shapes(sketch: Sketch, shapes: Sequence[Sequence[Vec2D]], background: int):
    if len(shapes) == 0:
        return

    if not isinstance(shapes[0], list):
        shapes = [shapes]

    sketch.fill(background)
    sketch.stroke(255, 255, 255, 3)
    sketch.begin_shape()
    # exterior part of shape, clockwise winding
    sketch.vertex(-2000, -2000)
    sketch.vertex(2000, -2000)
    sketch.vertex(2000, 2000)
    sketch.vertex(-2000, 2000)
    # interior part of shape, counter-clockwise winding
    for shape in shapes:
        sketch.begin_contour()
        for point in shape:
            sketch.vertex(point.x, point.y)
        sketch.end_contour()
    sketch.end_shape(sketch.CLOSE)
