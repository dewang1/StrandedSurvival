from characters import Characters
import pygame
from PIL import Image
import tempfile
import os

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
        self.sprite = self.get_sprite(Characters.PLAYER, sprite_index=0)
        super().__init__(x, y, size=50, image_path=self.sprite)

    def get_sprite(self, spritesheet_path, sprite_index):
        spritesheet = Image.open(spritesheet_path)
        sprite_width, sprite_height = 64, 64  # or whatever the size of each sprite is
        sprites_per_row = spritesheet.width // sprite_width
        x = (sprite_index % sprites_per_row) * sprite_width
        y = (sprite_index // sprites_per_row) * sprite_height
        sprite = spritesheet.crop((x, y, x + sprite_width, y + sprite_height))
        
        # Save the cropped image to a temporary file and return the file path
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        sprite.save(temp_file.name)
        return temp_file.name
    
    def walking_animation(self, sprite_index=14):
       # loop between two images (one with the character's right foot in front, and the next with the character's left foot in front)
        sprite1 = self.get_sprite(Characters.PLAYER, sprite_index)
        return sprite1
            
        
