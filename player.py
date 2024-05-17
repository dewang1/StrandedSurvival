from characters import Characters
import pygame
from PIL import Image

class Player:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = image  # This should be a pygame.Surface already

class HumanPlayer(Player):
    def __init__(self, x, y):
        self.spritesheet_path = Characters.PLAYER
        self.load_sprites()
        super().__init__(x, y, size=50, image=self.sprites['down'][0])
        self.current_direction = 'down'
        self.frame = 0
        self.frame_tick = 0  # Frame update ticker

    def load_sprites(self):
        """ Load all sprites from the spritesheet and store them in a dictionary. """
        sprite_width, sprite_height = 64, 64  # Adjust if different
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}
        directions = {'down': 10, 'left': 9, 'right': 11, 'up': 8}

        spritesheet = Image.open(self.spritesheet_path)
        for direction, row in directions.items():
            for col in range(9):  # 9 frames per direction
                x = col * sprite_width
                y = row * sprite_height
                sprite = spritesheet.crop((x, y, x + sprite_width, y + sprite_height))
                sprite_surface = pygame.image.fromstring(sprite.tobytes(), sprite.size, sprite.mode).convert_alpha()
                self.sprites[direction].append(sprite_surface)

        # Load the still frame (row 3, column 1)
        still_sprite = spritesheet.crop((0, 2 * sprite_height, 1 * sprite_width, 3 * sprite_height))
        self.still_sprite = pygame.image.fromstring(still_sprite.tobytes(), still_sprite.size, still_sprite.mode).convert_alpha()

    def move(self, dx, dy):
        """ Move player and update sprite based on direction. """
        moved = False
        if dx < 0:
            self.update_sprite('left')
            moved = True
        elif dx > 0:
            self.update_sprite('right')
            moved = True
        if dy < 0:
            self.update_sprite('up')
            moved = True
        elif dy > 0:
            self.update_sprite('down')
            moved = True

        if moved:
            self.x += dx
            self.y += dy
        else:
            self.reset_sprite()

    def update_sprite(self, direction):
        """ Update sprite to next frame in the current direction or change direction. """
        if self.current_direction != direction:
            self.current_direction = direction
            self.frame = 0
        if self.frame_tick >= 5:  # Adjust timing based on game speed
            self.frame = (self.frame + 1) % len(self.sprites[direction])
            self.frame_tick = 0
        else:
            self.frame_tick += 1
        self.image = self.sprites[direction][self.frame]

    def reset_sprite(self):
        """ Reset sprite to the first frame of the current direction. """
        self.image = self.sprites[self.current_direction][0]
        self.frame_tick = 0

    def draw(self, screen):
        """ Draw the current sprite at the player's position. """
        screen.blit(self.image, (self.x, self.y))
