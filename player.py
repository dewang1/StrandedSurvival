from characters import Characters
import pygame
from PIL import Image
from color import Color


class Player:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = image  # This should be a pygame.Surface already
        

class HumanPlayer(Player):
    def __init__(self, x, y, max_health, health):
        self.spritesheet_path = Characters.PLAYER
        self.load_sprites()
        super().__init__(x, y, size=50, image=self.sprites['down'][0])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.current_direction = 'down'
        self.frame = 1  # Start from the second frame for walking animation
        self.frame_tick = 0  # Frame update ticker
        self.max_health = max_health
        self.health = health

    def load_sprites(self):
        """ Load all sprites from the spritesheet and store them in a dictionary. """
        sprite_width, sprite_height = 64, 64  # Adjust if different
        self.sprites = {'down': [], 'left': [], 'right': [], 'up': []}
        self.still_sprites = {}  # Separate dictionary for still sprites
        directions = {'down': 10, 'left': 9, 'right': 11, 'up': 8}

        spritesheet = Image.open(self.spritesheet_path)
        for direction, row in directions.items():
            self.still_sprites[direction] = spritesheet.crop((0, row * sprite_height, sprite_width, (row + 1) * sprite_height))
            self.still_sprites[direction] = pygame.image.fromstring(self.still_sprites[direction].tobytes(), self.still_sprites[direction].size, self.still_sprites[direction].mode).convert_alpha()

            for col in range(1, 9):  # Frames 2-9 for walking animation
                x = col * sprite_width
                y = row * sprite_height
                sprite = spritesheet.crop((x, y, x + sprite_width, y + sprite_height))
                sprite_surface = pygame.image.fromstring(sprite.tobytes(), sprite.size, sprite.mode).convert_alpha()
                self.sprites[direction].append(sprite_surface)

    def move(self, dx, dy):
        """ Move player and update sprite based on direction. """
        moved = False
        if dy < 0:
            self.update_sprite('up')
            moved = True
        elif dy > 0:
            self.update_sprite('down')
            moved = True
        elif dx < 0:
            self.update_sprite('left')
            moved = True
        elif dx > 0:
            self.update_sprite('right')
            moved = True

        if moved:
            self.x += dx
            self.y += dy
            self.rect.topleft = (self.x, self.y)
        else:
            self.reset_sprite()

    def update_sprite(self, direction):
        """ Update sprite to next frame in the current direction or change direction. """
        if self.current_direction != direction:
            self.current_direction = direction
            self.frame = 1  # Start from the second frame for walking animation
        if self.frame_tick >= 1:  # Adjust timing based on game speed
            self.frame = (self.frame + 1) % len(self.sprites[direction])
            self.frame_tick = 0
        else:
            self.frame_tick += 1
        self.image = self.sprites[direction][self.frame - 1]

    def reset_sprite(self):
        """ Reset sprite to the first frame of the current direction. """
        self.image = self.still_sprites[self.current_direction]
        self.frame_tick = 0

    def draw_health_bar(self, screen):
        # Calculate health ratio
        health_ratio = self.health / self.max_health
        # Calculate health bar dimensions
        bar_width = self.size
        bar_height = 10
        health_bar_width = int(bar_width * health_ratio)

        # Draw the background of the health bar
        pygame.draw.rect(screen, "red", (self.rect.x, self.rect.y - 15, bar_width, bar_height))
        # Draw the health bar
        pygame.draw.rect(screen, "green", (self.rect.x, self.rect.y - 15, health_bar_width, bar_height))

    def draw(self, screen):
        """ Draw the current sprite at the player's position. """
        screen.blit(self.image, (self.x, self.y))
        self.draw_health_bar(screen)
 
    
    

# Enemies are colored squares for now (as templates)
class EnemyOne(Player):
	def __init__(self, x, y):
		super().__init__(x, y, size=50, color=Color.BLUE)

class EnemyTwo(Player):
	def __init__(self, x, y):
		super().__init__(x, y, size=50, color=Color.RED)

class EnemyThree(Player):
	def __init__(self, x, y):
		super().__init__(x, y, size=50, color=Color.YELLOW)
