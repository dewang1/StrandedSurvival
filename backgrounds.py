"""
File Name: backgrounds.py
Project Name: Choose Your Own Adventure Game: Stranded Survival: Island Escape
Team Members: Bhargav, Suchit, Derek
Date: 5/31/24
Task Description: This is the backgrounds file where the .tmx file background is being rendered in for each respective room.
"""

# backgrounds.py
from pytmx import load_pygame
import pygame
from collidable import Collidable

class Backgrounds:
    def __init__(self):
        self.tile_size = 16  # Assuming each tile is 16x16 pixels

    def load_tmx(self, path): # Loads the .tmx file path
        return load_pygame(path)

    def render_tmx(self, tmx_data, surface): # Goes through each layer on the tilemap and draws it in the correct position based on its id 
        # Render tile layers
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tile_size, y * self.tile_size))

        # Collect and sort all objects by their y-coordinate
        objects = []
        for layer in tmx_data.objectgroups:
            for obj in layer:
                objects.append(obj)
        objects.sort(key=lambda obj: obj.y)

        return objects

    def get_collidable_objects(self, tmx_data): # Makes an empty list to store the collidables in an object layer and takes the gid from the .tmx file. It returns the collidable objects. 

        collidables = []
        for layer in tmx_data.objectgroups:
            for obj in layer:
                collidable_rect = pygame.Rect(obj.x / 512 * 800, obj.y / 288 * 450, obj.width / 512 * 800, obj.height / 288 * 450)
                collidables.append(Collidable(collidable_rect, layer.name))
        return collidables
    
    def get_tmx_background(self, tmx_path): # The method loads the tilemap and adjusts the dimensions to fit the 800x450 dimensions in the game. It returns a tuple with the background surface, objects, and tile map data. 
        tmx_data = self.load_tmx(tmx_path)
        width = tmx_data.tilewidth * tmx_data.width
        height = tmx_data.tileheight * tmx_data.height
        background_surface = pygame.Surface((width, height))
        objects = self.render_tmx(tmx_data, background_surface)
        return background_surface, objects, tmx_data

    def JUNGLE(self): #This method calls get_tmx_background which then returns the tuple for the correct background to be displayed when in each room. 
        return self.get_tmx_background("backgrounds/JUNGLE.tmx")
    
    def BEACH(self):
        return self.get_tmx_background("backgrounds/BEACH.tmx")

    def CAVE(self):
        return self.get_tmx_background("backgrounds/CAVE.tmx")

    def MOUNTAIN(self):
        return self.get_tmx_background("backgrounds/MOUNTAIN.tmx")
    
    def OCEAN(self):
        return self.get_tmx_background("backgrounds/OCEAN.tmx")
    
    def POND(self):
        return self.get_tmx_background("backgrounds/POND.tmx")
