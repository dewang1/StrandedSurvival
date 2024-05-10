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


    def generate_setting(self):
        display = pygame.display.set_mode((self.width, self.height))
        image = pygame.image.load('backgrounds/riverBackground.jpg').convert_alpha()
        bg_image = pygame.transform.scale(image, (self.width, self.height))
        while True:
            display.blit(bg_image, (0, 0))
            pygame.draw.rect(self.screen, (53,115,0), pygame.Rect(100, 100, 600, 440))
            pygame.draw.ellipse(self.screen, (0,83,180), pygame.Rect(200, 150, 300, 180))
            pygame.display.update()
            self.clock.tick(self.clock_tick)

    def player(self):
        player = HumanPlayer(300, 300)

        pygame.draw.rect(self.screen, (255, 0, 0), (player.x, player.y, 50, 50))
        pygame.display.update()

    


    


def display():
    pygame.init()
    riverRoom = River()
    River.generate_setting(self=riverRoom)
    River.player(self=riverRoom)
    
    
        

display()