from py5 import Sketch


class Vision(object):
    def setup(self, sketch: Sketch):
        raise NotImplementedError

    def draw(self, sketch: Sketch):
        raise NotImplementedError

    def update(self, sketch: Sketch):
        raise NotImplementedError

    def handle_events(self, sketch: Sketch):
        raise NotImplementedError
