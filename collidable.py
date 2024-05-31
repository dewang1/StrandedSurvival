"""
File Name: collidable.py
Project Name: Choose Your Own Adventure Game: Stranded Survival: Island Escape
Team Members: Bhargav, Suchit, Derek
Date: 5/31/24
Task Description: Represents objects that can collide with other objects inside of the game.
"""
import pygame

class Collidable: 
    def __init__(self, rect, layer): #defines the position, size, and object layer
        self.rect = rect
        self.layer = layer
