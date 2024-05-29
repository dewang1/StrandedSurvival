from backgrounds import Backgrounds
from player import HumanPlayer, EnemyOne, EnemyTwo, EnemyThree
from color import Color
import pygame

class Screen:
    def __init__(self, internal_width=800, internal_height=450, background_property="BEACH", font_type="monospace", font_size=35, clock_tick=30):
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

        # Initialize background
        self.set_background(background_property)

    def set_background(self, background_property):
        self.current_background_property = background_property
        self.background = getattr(self.backgrounds, background_property)()
        self.background = pygame.transform.scale(self.background, (self.internal_width, self.internal_height))

    def handle_resize(self, event):
        self.window_width, self.window_height = event.size
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

	def refresh_background(self):
		self.screen.blit(self.background, (0, 0))

	def draw_healthbar(self, player):
		ratio = player.health / player.max_health
		pygame.draw.rect(self.screen, "red", (100, 600, 560, self.height))
		pygame.draw.rect(self.screen, "green", (100, 600, 560 * ratio, self.height))

	def draw_enemies(self, enemy_list):
		for enemy in enemy_list:
			enemy.draw(self.screen)

    def draw_player(self, player):
        player.draw(self.internal_surface)

    def update_screen(self, player):
        self.refresh_background()
        self.draw_player(player)

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
		self.draw_healthbar(player)
        self.clock.tick(self.clock_tick)        pygame.display.update()

