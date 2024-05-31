import pygame
from PIL import Image
from characters import Characters  # Ensure this import is correct

class Player:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = image  # This should be a pygame.Surface already

class HumanPlayer(Player):
    def __init__(self, x, y, max_health, health, max_hunger, hunger, max_temperature, temperature):
        self.spritesheet_path = Characters.PLAYER
        self.load_sprites()
        super().__init__(x, y, size=64, image=self.sprites['down'][0])
        self.current_direction = 'down'
        self.movement = 'stopped'
        self.frame = 1  # Start from the second frame for walking animation
        self.frame_tick = 0  # Frame update ticker
        self.last_key_press_time = 0
        self.key_press_threshold = 50  # Milliseconds
        self.max_health = max_health
        self.health = health

        # Initialize hunger and temperature attributes
        self.max_hunger = max_hunger
        self.hunger = hunger
        self.max_temperature = max_temperature
        self.temperature = temperature

        # Initialize inventory
        self.inventory = [{"item": None, "quantity": 0} for _ in range(9)]

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
        if dy < 0 and dx == 0:
            self.movement = 'up'
            self.update_sprite('up')
            moved = True
        elif dy > 0 and dx == 0:
            self.movement = 'down'
            self.update_sprite('down')
            moved = True
        elif dx < 0 and dy == 0:
            self.movement = 'left'
            self.update_sprite('left')
            moved = True
        elif dx > 0 and dy == 0:
            self.movement = 'right'
            self.update_sprite('right')
            moved = True
        elif dy < 0 and dx > 0:
            self.movement = 'up-right'
            if self.current_direction == 'right':
                self.update_sprite('right')  # Use 'right' sprite for diagonal up-right if 'right' was last pressed
            else:
                self.update_sprite('up')  # Use 'up' sprite for diagonal up-right if keys pressed at same time
            moved = True
        elif dy < 0 and dx < 0:
            self.movement = 'up-left'
            if self.current_direction == 'left':
                self.update_sprite('left')  # Use 'left' sprite for diagonal up-left if 'left' was last pressed
            else:
                self.update_sprite('up')  # Use 'up' sprite for diagonal up-left if keys pressed at same time
            moved = True
        elif dy > 0 and dx > 0:
            self.movement = 'down-right'
            if self.current_direction == 'right':
                self.update_sprite('right')  # Use 'right' sprite for diagonal down-right if 'right' was last pressed
            else:
                self.update_sprite('down')  # Use 'down' sprite for diagonal down-right if keys pressed at same time
            moved = True
        elif dy > 0 and dx < 0:
            self.movement = 'down-left'
            if self.current_direction == 'left':
                self.update_sprite('left')  # Use 'left' sprite for diagonal down-left if 'left' was last pressed
            else:
                self.update_sprite('down')  # Use 'down' sprite for diagonal down-left if keys pressed at same time
            moved = True
        elif dx != 0 or dy != 0:
            self.update_sprite(self.current_direction)
            moved = True

        if moved:
            self.x += dx
            self.y += dy
        else:
            self.movement = 'stopped'
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

    def draw(self, screen):
        """ Draw the current sprite at the player's position. """
        screen.blit(self.image, (self.x, self.y))

    def add_item(self, item, quantity):
        """ Add an item to the inventory. """
        for slot in self.inventory:
            if slot["item"] == item and slot["quantity"] < 20:
                slot["quantity"] = min(20, slot["quantity"] + quantity)
                return True
        for slot in self.inventory:
            if slot["item"] is None:
                slot["item"] = item
                slot["quantity"] = quantity
                return True
        return False


class Snake(Player):
    def __init__(self, x, y, venomous, length):
        # Initialize the parent Player class
        self.spritesheet_path = Characters.SNAKE  # Replace with the correct path to the snake sprite sheet
        self.sprites = self.load_sprites(self.spritesheet_path)
        super().__init__(x, y, size=64, image=self.sprites['slither'][0])  # Initial size and image
        self.venomous = venomous
        self.length = length
        self.frame = 0
        self.frame_tick = 0
        self.animation_speed = 5  # Adjust speed as needed

    def load_sprites(self, path):
        """ Load all sprites from the sprite sheet and store them in a dictionary. """
        sprite_width, sprite_height = 64, 64  # Adjust based on your sprite sheet dimensions
        spritesheet = Image.open(path)
        sprites = {'slither': []}

        # Extract slither frames from the first row
        for col in range(6):  # Assuming 6 frames for slithering animation
            x = col * sprite_width
            y = 0  # Only the first row
            sprite = spritesheet.crop((x, y, x + sprite_width, y + sprite_height))
            sprite_surface = pygame.image.fromstring(sprite.tobytes(), sprite.size, sprite.mode).convert_alpha()
            sprites['slither'].append(sprite_surface)

        return sprites

    def slither(self, dx, dy):
        """ Move snake and update sprite based on slither animation. """
        self.x += dx
        self.y += dy
        self.update_sprite('slither')

    def update_sprite(self, animation):
        """ Update sprite to next frame in the animation. """
        self.frame_tick += 1
        if self.frame_tick >= self.animation_speed:
            self.frame_tick = 0
            self.frame = (self.frame + 1) % len(self.sprites[animation])
            self.image = self.sprites[animation][self.frame]

    def attack(self, target):
        """ Attack method unique to Snake, can be expanded as needed. """
        if self.venomous:
            print(f"Attacking {target} with venom!")
        else:
            print(f"Attacking {target} with a bite!")

    def draw(self, screen):
        """ Draw the current sprite at the snake's position. """
        screen.blit(self.image, (self.x, self.y))
