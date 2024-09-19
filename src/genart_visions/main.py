import vision1
from importlib import reload
import os
import pygame

has_error = False
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
pygame.init()
screen = pygame.display.set_mode((1280, 1440))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30, bold = True)

def error_msg(screen):
    screen.fill((100, 50, 50));
    msg = font.render("Error - Reloading every 10 sec.", True, "gray")
    width, height = pygame.display.get_surface().get_size()
    screen.blit(msg, msg.get_rect(center=(width/2, height/2)))
    pygame.display.flip()

while True:
    try:
        vision1.main(clock, screen)
        has_error = False
    except:
        has_error = True
        error_msg(screen)
        input("")
        print("1", vision1.reload)

    if vision1.reload or has_error:
        print("2")
        reload(vision1)
    elif not has_error:
        exit()
