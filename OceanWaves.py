# oceanWaves.py
import pygame
import random

class OceanWaves:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("tiles/oceanWaves.png").convert_alpha()
        self.width, self.height = int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)  # Adjust this factor to change size
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.x = screen_width
        self.y = random.randint(0, screen_height - self.height)
        self.speed = random.uniform(2, 5)

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
