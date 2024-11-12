import argparse
import importlib
import os
import sys
import traceback
from pathlib import Path

os.environ["JAVA_HOME"] = "C:\Program Files\Microsoft\jdk-21.0.5.11-hotspot"


from py5 import Sketch

parser = argparse.ArgumentParser()
parser.add_argument("sketch_name")
args = parser.parse_args()
vision = importlib.import_module(args.sketch_name)


class MySketch(Sketch):
    def __init__(self):
        super().__init__()
        self.running = True

    def settings(self):
        self.size(1280, 1440)

    def setup(self):
        surface = self.get_surface()
        surface.set_location(0, 0)
        vision.viz.setup(self)

    def predraw_update(self):
        vision.viz.update()

    def draw(self):
        vision.viz.draw(self)

    def key_pressed(self):
        if self.key == "r":
            try:
                for path in Path(__file__).parent.glob("*"):
                    if any([s in path.name for s in ["__pycache__", "main", "test1"]]):
                        continue
                    mod_name = path.name.split(".")[0]
                    if mod_name in sys.modules.keys():
                        importlib.reload(sys.modules[mod_name])

                self.frame_count = 0
                vision.viz.setup(self)
            except Exception:
                print(traceback.format_exc())
        if self.key == "q":
            self.exit_sketch()
        if self.key == "s":
            if self.running:
                self.no_loop()
                self.running = False
            else:
                self.loop()
                self.running = True


test = MySketch()
test.run_sketch()
