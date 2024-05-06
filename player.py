from characters import Characters
import pygame

class Player:
    def __init__(self, x, y, size, image_path=Characters.PLAYER):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.image.load(image_path).convert_alpha()  # Load and convert the image at initialization

    def draw(self, screen):
        # Blit the loaded image onto the screen at the player's position
        screen.blit(self.image, (self.x, self.y))

    def detect_collision(self, other):
        if (other.x >= self.x and other.x < (self.x + self.size)) or (self.x >= other.x and self.x < (other.x + other.size)):
            if (other.y >= self.y and other.y < (self.y + self.size)) or (self.y >= other.y and self.y < (other.y + other.size)):
                return True
        return False

class Enemy(Player):
    def __init__(self, x, y):
        super().__init__(x, y, size=50, image_path=Characters.ENEMY)  # Make sure the Characters.ENEMY path is correct

class HumanPlayer(Player):
    def __init__(self, x, y):
        super().__init__(x, y, size=50, image_path=Characters.PLAYER)
