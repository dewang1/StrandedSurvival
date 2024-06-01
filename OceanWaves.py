"""
Names: Derek Wang, Suchit Basineni, Bhargav Yerramsetty
Date: 5/31/2024
OceanWaves.py
Description: This file contains the OceanWaves class, which is responsible for rendering ocean waves on the screen.
"""
import pygame
import random

class OceanWaves:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("tiles/oceanWaves.png").convert_alpha()
        self.width, self.height = int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)  # Adjust this factor to change size
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Wave starts off-screen to the right
        self.x = screen_width
        # Randomize the y-coordinate of the wave
        self.y = random.randint(0, screen_height - self.height)

        # Randomize the speed of the wave
        self.speed = random.uniform(2, 5)

    # Move the wave to the left
    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    # Get the hitbox of the wave
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
