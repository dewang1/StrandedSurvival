from PIL import Image
import pygame


class Backgrounds:
    _loaded_images = {}

    @classmethod
    def load_image(cls, path):
        if path not in cls._loaded_images:
            cls._loaded_images[path] = pygame.image.load(path).convert()
        return cls._loaded_images[path]

    def BEACH(self):
        return self.load_image("backgrounds/beachBackground.jpg")

    def CAVE(self):
        return self.load_image("backgrounds/caveBackground.jpg")

    def MOUNTAIN(self):
        return self.load_image("backgrounds/mountainBackground.jpg")

    def OCEAN(self):
        return self.load_image("backgrounds/oceanBackground.png")

    def RIVER(self):
        return self.load_image("backgrounds/riverBackground.jpg")
    
    def JUNGLE(self):
        return self.load_image("backgrounds/jungleBackground.jpg")

