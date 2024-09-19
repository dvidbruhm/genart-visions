# Example file showing a basic pygame "game loop"
import os
import pygame
import pygame.gfxdraw as gfxdraw
from utils import get_random_pos
import random
import perlin_noise
import math
from flowfield import Flowfield
from particle import Particle
from sketch import Sketch


class Vision1(Sketch):
    def __init__(self, n_part=100, flowfield_res=10):
        super(Vision1, self).__init__()
        width, height = pygame.display.get_surface().get_size()
        self.flowfield = Flowfield(flowfield_res, height, width)
        self.flowfield.create_field()
        self.particles = [Particle(get_random_pos(width, height), 2, 1, 3, height, width) for _ in range(n_part)]

    def draw(self, screen):
        screen.fill(0)
        self.flowfield.display(screen)
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
def main(clock, screen):
    global reload
    sketch = Vision1(1000, 10)
    #os.system("xte 'keydown Alt_L' 'keydown Tab' 'keyup Alt_L' 'keyup Tab'")
    while not reload:
        clock.tick(60)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reload = True

        sketch.handle_events(pygame.event.get())
        sketch.update()
        sketch.draw(screen)
        pygame.display.flip()
