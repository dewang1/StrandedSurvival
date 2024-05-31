import pygame
from backgrounds import Backgrounds
from player import HumanPlayer
from color import Color

class CollisionObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Screen:
    def __init__(self, internal_width=800, internal_height=450, background_property="BEACH", font_type="monospace", font_size=18, clock_tick=30):
        pygame.display.init()
        self.internal_width = internal_width
        self.internal_height = internal_height
        self.internal_surface = pygame.Surface((internal_width, internal_height))
        self.background_surface = pygame.Surface((512, 288), pygame.SRCALPHA)
        self.background_surface.fill((0, 0, 0, 0))  # fill with fully transparent color
        self.screen = pygame.display.set_mode((internal_width, internal_height), pygame.RESIZABLE)
        self.backgrounds = Backgrounds()
        self.font = pygame.font.SysFont(font_type, font_size)
        self.clock = pygame.time.Clock()
        self.clock_tick = clock_tick
        self.current_background_property = background_property
        self.window_width = internal_width
        self.window_height = internal_height
        self.collidable_objects = []  # List to store collidable objects

        # Load heart spritesheet
        self.hearts_spritesheet = pygame.image.load("UI/Health_04_Heart_Red_Clear.png").convert_alpha()
        self.heart_width, self.heart_height = 48, 48
        self.heart_scale_factor = 0.83  # Scale hearts to 83% of original size
        self.scaled_heart_height = int(self.heart_height * self.heart_scale_factor)

        # Load inventory image
        self.inventory_image = pygame.image.load("UI/Inventory_Example_03.png").convert_alpha()

        # Initialize background and objects
        self.set_background(background_property)

        # Load hunger and temperature bars
        self.hunger_bar_image = pygame.image.load("UI/Health_01_Bar02.png").convert_alpha()
        self.temperature_bar_image = pygame.image.load("UI/Health_01_Bar03.png").convert_alpha()
        self.bar_width, self.bar_height = 183, 48
        self.bar_crop_width = 135
        self.bar_scale_factor = 1.2  # Scale bars to 120% of original size

        # Load icons
        self.hunger_icon = pygame.image.load("UI/hunger.png").convert_alpha()
        self.temperature_icon = pygame.image.load("UI/snowflake.png").convert_alpha()

        # Scale icons to fit the left empty space of the bars
        self.hunger_icon = pygame.transform.scale(self.hunger_icon, (int(23 * self.bar_scale_factor), int(23 * self.bar_scale_factor)))
        self.temperature_icon = pygame.transform.scale(self.temperature_icon, (int(23 * self.bar_scale_factor), int(23 * self.bar_scale_factor)))

    def set_background(self, background_property):
        self.current_background_property = background_property
        self.background, self.objects, tmx_data = getattr(self.backgrounds, background_property)()
        self.current_background_path = f"backgrounds/{background_property}.tmx"
        self.background = pygame.transform.scale(self.background, (self.internal_width, self.internal_height))

        # Load collidable objects for the new background
        self.collidable_objects = self.backgrounds.get_collidable_objects(tmx_data)

    def handle_resize(self, event):
        self.window_width, self.window_height = event.size
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

    def refresh_background(self):
        self.internal_surface.blit(self.background, (0, 0))

    def draw_hearts(self, player):
        health_per_heart = 4  # Each heart represents 4 health points
        hearts = player.max_health // health_per_heart

        scaled_heart_width = int(self.heart_width * self.heart_scale_factor)

        for i in range(hearts):
            if player.health >= (i + 1) * health_per_heart:
                heart_state = 0  # Full heart
            else:
                remaining_health = player.health - i * health_per_heart
                if remaining_health >= 3:
                    heart_state = 1  # 3/4 heart
                elif remaining_health >= 2:
                    heart_state = 2  # 1/2 heart
                elif remaining_health >= 1:
                    heart_state = 3  # 1/4 heart
                else:
                    heart_state = 4  # Empty heart

            heart_image = self.hearts_spritesheet.subsurface(
                (heart_state * self.heart_width, 0, self.heart_width, self.heart_height)
            )
            scaled_heart_image = pygame.transform.scale(heart_image, (scaled_heart_width, self.scaled_heart_height))
            self.internal_surface.blit(scaled_heart_image, (10 + i * (scaled_heart_width + 5), self.internal_height - self.scaled_heart_height - 10))

    def draw_bars(self, player):
        hunger_ratio = player.hunger / player.max_hunger
        temperature_ratio = player.temperature / player.max_temperature

        scaled_bar_width = int(self.bar_width * self.bar_scale_factor)
        scaled_bar_height = int(self.bar_height * self.bar_scale_factor)

        cropped_hunger_bar = self.hunger_bar_image.subsurface(
            (48, 0, hunger_ratio * self.bar_crop_width, self.bar_height)
        )
        cropped_temperature_bar = self.temperature_bar_image.subsurface(
            (48, 0, temperature_ratio * self.bar_crop_width, self.bar_height)
        )

        scaled_hunger_bar = pygame.transform.scale(cropped_hunger_bar, (int(hunger_ratio * self.bar_crop_width * self.bar_scale_factor), scaled_bar_height))
        scaled_temperature_bar = pygame.transform.scale(cropped_temperature_bar, (int(temperature_ratio * self.bar_crop_width * self.bar_scale_factor), scaled_bar_height))

        # Blit hunger icon and bar
        self.internal_surface.blit(self.hunger_icon, (15, self.internal_height - self.scaled_heart_height - scaled_bar_height + 11))
        self.internal_surface.blit(scaled_hunger_bar, (58, self.internal_height - self.scaled_heart_height - scaled_bar_height + 3))

        # Blit temperature icon and bar
        self.internal_surface.blit(self.temperature_icon, (15, self.internal_height - self.scaled_heart_height - 2 * scaled_bar_height + 17))
        self.internal_surface.blit(scaled_temperature_bar, (58, self.internal_height - self.scaled_heart_height - 2 * scaled_bar_height + 9))

    def draw_player(self, player):
        player.draw(self.internal_surface)

    def draw_collidable_objects(self):
        for obj in self.collidable_objects:
            pygame.draw.rect(self.internal_surface, (255, 0, 0), obj, 2)  # Draw the collidables in red

    def draw_translucent_box(self):
        # Define the dimensions and position of the box
        box_width = 240
        box_height = 140
        box_x = 5
        box_y = self.internal_height - box_height - 10

        # Define the color and transparency (RGBA format)
        translucent_gray = (128, 128, 128, 128)  # Gray color with 50% opacity

        # Create a surface with per-pixel alpha
        translucent_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        translucent_box.fill(translucent_gray)

        # Blit the translucent box onto the internal surface
        self.internal_surface.blit(translucent_box, (box_x, box_y))

    def draw_inventory(self, player):
        """ Draw the inventory on the screen. """
        scaled_inventory = pygame.transform.scale(self.inventory_image, (250, 250))
        inventory_x = (self.internal_width - scaled_inventory.get_width()) // 2
        inventory_y = (self.internal_height - scaled_inventory.get_height()) // 2
        self.internal_surface.blit(scaled_inventory, (inventory_x, inventory_y))

        # Draw items in the inventory
        slot_size = 40
        for i, slot in enumerate(player.inventory):
            x = inventory_x + 10 + (i % 3) * (slot_size + 31)
            y = inventory_y + 10 + (i // 3) * (slot_size + 31)
            if slot["item"]:
                item_image = pygame.image.load(f"items/{slot['item']}.png").convert_alpha()
                # Get the original image dimensions
                original_width, original_height = item_image.get_size()

                # Calculate the aspect ratio
                aspect_ratio = original_width / original_height

                # Calculate the new dimensions
                if original_width > original_height:
                    new_width = slot_size
                    new_height = int(slot_size / aspect_ratio)
                else:
                    new_width = int(slot_size * aspect_ratio)
                    new_height = slot_size

                # Scale the image
                item_image = pygame.transform.scale(item_image, (new_width, new_height))
                self.internal_surface.blit(item_image, (x + 20, y + 25))
                self.font.set_bold(True) 
                quantity_text = self.font.render(str(slot["quantity"]), True, (255, 255, 255))
                self.internal_surface.blit(quantity_text, (x + slot_size + 7, y + slot_size + 12))
                self.font.set_bold(False) 

    def draw_cooldown_bar(self, cooldown_ratio):
        bar_width = 100
        bar_height = 20
        bar_x = self.internal_width - bar_width - 20
        bar_y = 20

        # Draw the background of the bar
        pygame.draw.rect(self.internal_surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Draw the foreground of the bar
        cooldown_width = int(bar_width * cooldown_ratio)
        pygame.draw.rect(self.internal_surface, (200, 200, 200), (bar_x, bar_y, cooldown_width, bar_height))

    def update_screen(self, player, inventory_open, cooldown_ratio=1):
        self.refresh_background()

        # Calculate the scaling factors
        scale_factor_y = self.internal_height / 288

        # Combine objects and player into a single list
        all_sprites = [(obj.x, obj.y, obj.y * scale_factor_y  + obj.height * scale_factor_y, obj.gid) for obj in self.objects]
        all_sprites.append((player.x, player.y, player.y + player.size, player))

        # Sort all sprites by their y-coordinate
        all_sprites.sort(key=lambda sprite: sprite[2])


        # Draw all sprites in sorted order
        tmx_data = self.backgrounds.load_tmx(self.current_background_path)
        for sprite in all_sprites:
            if isinstance(sprite[3], HumanPlayer):
                sprite[3].draw(self.internal_surface)
                pygame.draw.circle(self.internal_surface, Color.RED, (sprite[3].x, sprite[3].y), 5) 
                player_rect = pygame.Rect(player.x + 20 , player.y + 40, player.size - 40, player.size - 40)
                pygame.draw.rect(self.internal_surface, (255, 0, 0), player_rect, 2)  
            else:
                tile = tmx_data.get_tile_image_by_gid(sprite[3])
                if tile:
                    self.background_surface.blit(tile, (sprite[0], sprite[1]))
                    transformed_surface = pygame.transform.scale(self.background_surface, (self.internal_width, self.internal_height))
                    self.internal_surface.blit(transformed_surface, (0, 0))
                    self.background_surface.fill((0, 0, 0, 0))  # fill with fully transparent color
        self.draw_collidable_objects()
        self.draw_translucent_box()
        self.draw_bars(player)
        self.draw_hearts(player)

        if inventory_open:
            self.draw_inventory(player)

        if cooldown_ratio < 1:
            self.draw_cooldown_bar(cooldown_ratio)

        # Calculate the scaling factors
        scale_x = self.window_width / self.internal_width
        scale_y = self.window_height / self.internal_height

        # Maintain the aspect ratio
        if scale_x < scale_y:
            scale_factor = scale_x
            scaled_width = self.window_width
            scaled_height = int(self.internal_height * scale_factor)
            offset_x = 0
            offset_y = (self.window_height - scaled_height) // 2
        else:
            scale_factor = scale_y
            scaled_width = int(self.internal_width * scale_factor)
            scaled_height = self.window_height
            offset_x = (self.window_width - scaled_width) // 2
            offset_y = 0

        scaled_surface = pygame.transform.scale(self.internal_surface, (scaled_width, scaled_height))
        self.screen.fill((0, 0, 0))  # Fill with black
        self.screen.blit(scaled_surface, (offset_x, offset_y))
        self.clock.tick(self.clock_tick)
        pygame.display.update()
