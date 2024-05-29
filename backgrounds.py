from pytmx import load_pygame
import pygame

class Backgrounds:
    def __init__(self):
        self.tile_size = 16  # Assuming each tile is 32x32 pixels

    def load_tmx(self, path):
        return load_pygame(path)

    def render_tmx(self, tmx_data, surface):
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tile_size, y * self.tile_size))

    def get_tmx_background(self, tmx_path):
        tmx_data = self.load_tmx(tmx_path)
        width = tmx_data.tilewidth * tmx_data.width
        height = tmx_data.tileheight * tmx_data.height
        background_surface = pygame.Surface((width, height))
        self.render_tmx(tmx_data, background_surface)
        return background_surface

    def JUNGLE(self):
        return self.get_tmx_background("map/jungle.tmx")
    
    def BEACH(self):
        return self.get_tmx_background("map/beachplaceholder.tmx")
    
    def OCEAN(self):
        return self.get_tmx_background("map/ocean.tmx")
