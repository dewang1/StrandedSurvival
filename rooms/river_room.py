import pygame
import sys
sys.path.insert(0, './')
from player import HumanPlayer



class River:
    def __init__(self, width=800, height=640, font_type="monospace", font_size=35, clock_tick=60):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(font_type, font_size)
        self.clock = pygame.time.Clock()
        self.clock_tick = clock_tick
