from pytmx import load_pygame
import pygame

class Backgrounds:
    def __init__(self):
        self.tile_size = 16  # Assuming each tile is 16x16 pixels

    def load_tmx(self, path):
        return load_pygame(path)

    def render_tmx(self, tmx_data, surface):
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

    def get_tmx_background(self, tmx_path):
        tmx_data = self.load_tmx(tmx_path)
        width = tmx_data.tilewidth * tmx_data.width
        height = tmx_data.tileheight * tmx_data.height
        background_surface = pygame.Surface((width, height))
        objects = self.render_tmx(tmx_data, background_surface)
        return background_surface, objects

    def JUNGLE(self):
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
