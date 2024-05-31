"""
Names: Derek Wang, Suchit Basineni, Bhargav Yerramsetty
Date: 5/31/2024
collidable.py
Description: This file contains the Collidable class, which is responsible for storing information about collidable objects.
"""

# Import the pygame library
import pygame

# Define a class for collidable objects
class Collidable:
    # Initialize a Collidable object with a rectangle and a layer
    def __init__(self, rect, layer):
        self.rect = rect
        self.layer = layer