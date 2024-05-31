import pygame
from backgrounds import Backgrounds
from player import HumanPlayer
from color import Color

class CollisionObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Screen:
    def __init__(self, internal_width=800, internal_height=450, background_property="JUNGLE", font_type="monospace", font_size=35, clock_tick=30):
        pygame.display.init()
        self.internal_width = internal_width
        self.internal_height = internal_height
        self.internal_surface = pygame.Surface((internal_width, internal_height))
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

        # Load and position inventory icon
        self.inventory_icon = pygame.image.load("UI/Inventory_Example_03.png").convert_alpha()
        self.inventory_icon = pygame.transform.scale(self.inventory_icon, (int(200), int(200)))
        self.inventory_icon_rect = self.inventory_icon.get_rect(topright=(self.internal_width - 10, 10))
        self.show_inventory = False

    def set_background(self, background_property):
        self.current_background_property = background_property
        self.background, tmx_data = getattr(self.backgrounds, background_property)()
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

    def draw_inventory_popup(self):
        inventory_surface = pygame.Surface((self.internal_width // 2, self.internal_height // 2))
        inventory_surface.fill((50, 50, 50))
        inventory_rect = inventory_surface.get_rect(center=(self.internal_width // 2, self.internal_height // 2))
        self.internal_surface.blit(inventory_surface, inventory_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.inventory_icon_rect.collidepoint(event.pos):
                    self.show_inventory = not self.show_inventory

    def update_screen(self, player):
        self.handle_events()
        self.refresh_background()
        self.draw_player(player)
        self.draw_bars(player)
        self.draw_hearts(player)

        # Draw inventory icon
        self.internal_surface.blit(self.inventory_icon, self.inventory_icon_rect)

        # Draw inventory popup if toggled
        if self.show_inventory:
            self.draw_inventory_popup()

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

# Ensure to update your asset path and names as needed.
# Make sure to load the `inventory_icon.png` in the same way as other images.
