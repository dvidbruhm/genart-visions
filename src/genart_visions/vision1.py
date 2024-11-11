import flowfield
import particle
import pygame
import pyglet
import sketch
import utils


class Vision1(sketch.Sketch):
    def __init__(self, screen, n_part=100, flowfield_res=10):
        super(Vision1, self).__init__()
        width, height = screen.get_size()
        self.flowfield = flowfield.Flowfield(flowfield_res, height, width)
        self.flowfield.create_field()
        self.particles = [
            particle.Particle(
                utils.get_random_pos(width, height),
                2,
                5,
                30,
                height,
                width,
                pygame.Color(200, 192, 147),
            )
            for _ in range(n_part)
        ]
        self.batch = pyglet.graphics.Batch()

    def draw(self, screen):
        screen.fill((31, 31, 40))
        # self.flowfield.display(screen)
        for p in self.particles:
            p.display(screen)

    def update(self):
        for p in self.particles:
            p.update(self.flowfield)

    def handle_events(self, events):
        # for e in events:
        #     if e.type == KEYDOWN and e.key == K_SPACE:
        #         pass
        pass


reload = False


def main(clock, screen: pygame.Surface):
    global reload
    translated_screen = pygame.Surface((1000, 1000))
    screen.fill(pygame.Color(22, 22, 29))
    sketch = Vision1(translated_screen, 100, 10)
    while not reload:
        clock.tick(60)

        reload = utils.sketch_events()

        sketch.handle_events(pygame.event.get())
        sketch.update()
        sketch.draw(translated_screen)

        screen.blit(translated_screen, (140, 220))
        pygame.display.flip()


def main2():
    batch = pyglet.graphics.Batch()
    sketch = Vision1(batch)
    pyglet.app.run()


if __name__ == "__main__":
    main2()
