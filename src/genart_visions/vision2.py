import lib.utils as libutils
import vision
from py5 import Sketch

OUTPUT_PATH = "output/" + __name__


class Vision2(vision.Vision):
    def __init__(self, width: int, height: int, steps: int = 0) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.steps = steps

    def setup(self, sketch: Sketch) -> None:
        self.background = sketch.color(31, 31, 40)
        sketch.no_stroke()
        sketch.rect_mode(sketch.CENTER)
        sketch.loop()
        self.on_restart(sketch)

    def save_sketch(self, sketch: Sketch) -> None:
        p = libutils.get_file_name(OUTPUT_PATH)
        sketch.save(p)

    def on_restart(self, sketch: Sketch) -> None:
        sketch.rect_mode(sketch.CENTER)
        sketch.background(22, 22, 29)
        sketch.fill(self.background)
        sketch.no_stroke()
        sketch.rect(sketch.width / 2, sketch.height / 2, self.width, self.height)

    def update(self, sketch: Sketch):
        pass

    def draw(self, sketch: Sketch):
        # Outside border
        sketch.push()
        self.on_restart(sketch)
        sketch.translate(140, 220)
        sketch.clip(0, 0, self.width, self.height)

        # Start sketch
        sketch.fill(0)
        sketch.circle(500, 500, 40)

        # End sketch
        if self.steps != 0 and sketch.frame_count > self.steps:
            sketch.no_loop()
            self.save_sketch(sketch)

        sketch.pop()


libutils.mkdir(OUTPUT_PATH)

viz = Vision2(1000, 1000, steps=0)
