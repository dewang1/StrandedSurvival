import pygame

class Collidable:
    def __init__(self, rect, layer):
        self.rect = rect
        self.layer = layer
