import flowfield
import flowfield_type
import lib.primitives as pr
import lib.utils as libutils
import particle
import utils
import vision
from py5 import Sketch

OUTPUT_PATH = "output/" + __name__


class Vision1(vision.Vision):
    def __init__(self, width: int, height: int, steps: int = 0, n_part: int = 100, flowfield_res: int = 10) -> None:
        super().__init__()
        self.flowfield_res = flowfield_res
        self.n_part = n_part
        self.width = width
        self.height = height
        self.steps = steps

    def save_sketch(self, sketch: Sketch):
        p = libutils.get_file_name(OUTPUT_PATH)
        sketch.save(p)

    def on_restart(self, sketch: Sketch):
        sketch.rect_mode(sketch.CENTER)
        sketch.background(22, 22, 29)
        sketch.fill(self.background)
        sketch.no_stroke()
        sketch.rect(sketch.width / 2, sketch.height / 2, self.width, self.height)

    def setup(self, sketch: Sketch):
        self.image = sketch.load_image("C:\\Projects\\genart-visions\\data\\test1-transformed.jpeg")
        # from_image = FromImage()
        # from_image.setup(image=self.image)
        fftype = flowfield_type.Noise(0.001)
        self.flowfield = flowfield.Flowfield(sketch, self.flowfield_res, self.width, self.height, fftype)

        self.background = sketch.color(31, 31, 40)

        self.circles = []
        for x, y in pr.circle_points(500, 500, 300, 5):
            self.circles.append(pr.circle_points(x, y, 150, 200))
        self.rects = []
        self.rect = pr.rect_points(300, 300, 200, 430, 50)
        self.circles.append(self.rect)

        choices = [x for xs in self.circles for x in xs]

        self.particles = [self.new_particle(sketch) for _ in range(self.n_part)]
        a = utils.Vec2D(100, 100)
        b = utils.Vec2D(200, 200)

        sketch.no_stroke()
        sketch.rect_mode(sketch.CENTER)
        sketch.loop()
        self.on_restart(sketch)
        # pr.sand_line(sketch)

    def new_particle(self, sketch: Sketch) -> particle.Particle:
        return particle.Particle(
            utils.get_random_2d_pos(self.width, self.height),
            # utils.get_random_1d_pos(utils.Vec2D(0, 0), utils.Vec2D(0, self.height)),
            # sketch.random_choice(pr.rect_points(20, 20, 960, 960, 200)),
            3,
            5,
            500,
            self.height,
            self.width,
            sketch.color(200, 192, 147, 100),
            varying_width=False,
            acceleration=0.4,
            friction=0.94,
            wrap=True,
        )

    def update(self, sketch: Sketch):
        for p in self.particles:
            if not p.active:
                continue
            p.update(self.flowfield)
            p.collision_all(self.particles)
            if not p.active:
                self.particles.append(self.new_particle(sketch))

    def draw(self, sketch: Sketch):
        sketch.push()
        # Outside border
        self.on_restart(sketch)

        # Start sketch
        sketch.translate(140, 220)
        sketch.clip(0, 0, self.width, self.height)

        # sketch.tint(255, 5)
        # sketch.image(self.image, 0, 0)
        for p in self.particles:
            p.display(sketch)

        # pr.extrude_shapes(sketch, self.circles, sketch.color(31, 31, 40, 250))

        # self.flowfield.display()

        # End sketch
        if self.steps != 0 and sketch.frame_count > self.steps:
            sketch.no_loop()
            self.save_sketch(sketch)

        sketch.pop()


libutils.mkdir(OUTPUT_PATH)

viz = Vision1(1000, 1000, steps=0, n_part=500, flowfield_res=20)
