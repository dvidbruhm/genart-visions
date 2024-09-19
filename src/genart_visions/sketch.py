class Sketch(object):
    def __init__(self):
        pass

    def draw(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
