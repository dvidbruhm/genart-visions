import flowfield
import particle
import utils
import vision
from py5 import Sketch


class Vision1(vision.Vision):
    def __init__(self, width: int, height: int, steps: int = 0, n_part: int = 100, flowfield_res: int = 10) -> None:
        super().__init__()
        self.flowfield_res = flowfield_res
        self.n_part = n_part
        self.width = width
        self.height = height
        self.steps = steps

    def setup(self, sketch: Sketch):
        self.flowfield = flowfield.Flowfield(sketch, self.flowfield_res, self.width, self.height)
        self.flowfield.create_field(sketch, 0.03)
        self.particles = [
            particle.Particle(utils.get_random_pos(self.width, self.height), 3, 2, 10, self.height, self.width, (200, 192, 147), varying_width=False)
            for _ in range(self.n_part)
        ]
        sketch.no_stroke()
        sketch.rect_mode(sketch.CENTER)
        sketch.loop()

    def update(self):
        for p in self.particles:
            p.update(self.flowfield)

    def draw(self, sketch: Sketch):
        sketch.background(22, 22, 29)
        sketch.fill(31, 31, 40)
        sketch.no_stroke()
        sketch.rect(sketch.width / 2, sketch.height / 2, self.width, self.height)
        sketch.translate(140, 220)

        # self.flowfield.create_field(sketch, 0.04)
        # self.flowfield.display(sketch)

        for p in self.particles:
            p.display(sketch)

        sketch.translate(500, 500)
        sketch.begin_shape()
        sketch.begin_contour()
        sketch.vertex(-200, -200)
        sketch.vertex(-200, 200)
        sketch.vertex(200, 200)
        sketch.vertex(200, -200)
        sketch.end_contour()
        sketch.end_shape(sketch.CLOSE)

        if self.steps != 0 and sketch.frame_count > self.steps:
            sketch.no_loop()


viz = Vision1(1000, 1000, steps=0, n_part=500, flowfield_res=5)
