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
        self.key_press_threshold = 50 
        self.max_health = max_health
        self.health = health

        # Initialize hunger and temperature attributes
        self.max_hunger = max_hunger
        self.hunger = hunger
        self.max_temperature = max_temperature
        self.temperature = temperature

        # Initialize inventory
        self.inventory = [{"item": None, "quantity": 0} for _ in range(9)]

        # Initialize spear flag
        self.has_spear = False

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
        max_stack_size = 30

        # First, try to add the item to existing stacks
        for slot in self.inventory:
            if slot["item"] == item:
                if slot["quantity"] < max_stack_size:
                    available_space = max_stack_size - slot["quantity"]
                    add_quantity = min(quantity, available_space)
                    slot["quantity"] += add_quantity
                    quantity -= add_quantity
                    if quantity <= 0:
                        return True

        # Then, try to add the remaining quantity to new slots
        for slot in self.inventory:
            if slot["item"] is None:
                add_quantity = min(quantity, max_stack_size)
                slot["item"] = item
                slot["quantity"] = add_quantity
                quantity -= add_quantity
                if quantity <= 0:
                    return True

        # If there is remaining quantity and no slots available, it cannot be added
        return False

    def clear_inventory_slot(self, slot_index):
        """ Clear the specified inventory slot. """
        if 0 <= slot_index < len(self.inventory):
            self.inventory[slot_index] = {"item": None, "quantity": 0}

    def check_crafting_requirements(self):
        spear_requirements = {"wood": 1, "rock": 1, "vine": 1}
        torch_requirements = {"wood": 1, "vine": 1, "leaf": 1, "coal": 1}
        pulley_requirements = {"wood": 4, "vine": 5}

        can_craft_spear = all(
            any(slot["item"] == item and slot["quantity"] >= quantity for slot in self.inventory)
            for item, quantity in spear_requirements.items()
        ) and not self.has_spear

        can_craft_torch = all(
            any(slot["item"] == item and slot["quantity"] >= quantity for slot in self.inventory)
            for item, quantity in torch_requirements.items()
        ) and not self.has_item_in_inventory("torch")

        can_craft_pulley = all(
            any(slot["item"] == item and slot["quantity"] >= quantity for slot in self.inventory)
            for item, quantity in pulley_requirements.items()
        ) and not self.has_item_in_inventory("pulley")

        return can_craft_spear, can_craft_torch, can_craft_pulley


    def craft_item(player, crafted_item, required_items):
        for req_item, req_quantity in required_items.items():
            for slot in player.inventory:
                if slot["item"] == req_item and slot["quantity"] > 0:
                    slot["quantity"] -= req_quantity
                    if slot["quantity"] <= 0:
                        slot["item"] = None
                        slot["quantity"] = 0
                    break

    def has_item_in_inventory(self, item_name):
        """ Check if the player has an item in their inventory. """
        return any(slot["item"] == item_name for slot in self.inventory)
    
    def is_inventory_full(self):
        return all(slot["item"] is not None for slot in self.inventory)

