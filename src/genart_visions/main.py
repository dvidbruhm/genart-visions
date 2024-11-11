import importlib
import traceback
import os
from pathlib import Path
import pygame
import argparse
from types import ModuleType
import sys
import glob
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

parser = argparse.ArgumentParser()
parser.add_argument("sketch_name")
args = parser.parse_args()
vision = importlib.import_module(args.sketch_name)

has_error = False
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0, 0)
pygame.init()
screen = pygame.display.set_mode((1280, 1440))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30, bold=True)


def error_msg(screen):
    screen.fill((100, 50, 50))
    msg = font.render("Error - Reloading every 10 sec.", True, "gray")
    width, height = pygame.display.get_surface().get_size()
    screen.blit(msg, msg.get_rect(center=(width / 2, height / 2)))
    pygame.display.flip()


while True:
    try:
        vision.main(clock, screen)
        has_error = False
    except Exception as e:
        has_error = True
        error_msg(screen)
        print(traceback.format_exc())
        input("")

    if vision.reload or has_error:
        for path in Path(__file__).parent.glob("*"):
            if any([s in path.name for s in ["__pycache__", "main"]]):
                continue
            mod_name = path.name.split(".")[0]
            if mod_name in sys.modules.keys():
                importlib.reload(sys.modules[mod_name])
    elif not has_error:
        exit()
