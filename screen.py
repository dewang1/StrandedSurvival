from backgrounds import Backgrounds
from player import HumanPlayer, EnemyOne, EnemyTwo, EnemyThree
from color import Color
import pygame

class Screen:
	def __init__(self, width=800, height=640, background_property="BEACH", font_type="monospace", font_size=35, clock_tick=30):
		pygame.display.init()
		self.screen = pygame.display.set_mode((width, height))
		self.backgrounds = Backgrounds()
		self.set_background(background_property)
		self.width = width
		self.height = height
		self.font = pygame.font.SysFont(font_type, font_size)
		self.clock = pygame.time.Clock()
		self.clock_tick = clock_tick

	def set_background(self, background_property):
		self.background = getattr(self.backgrounds, background_property)()


	def refresh_background(self):
		self.screen.blit(self.background, (0, 0))


	def draw_enemies(self, enemy_list):
		for enemy in enemy_list:
			enemy.draw(self.screen)

	def draw_player(self, player):
		player.draw(self.screen)

	def draw_inventory_button(self, button_rect):
		pygame.draw.rect(self.screen, (0, 0, 255), button_rect)  # Blue button
		text_surface = self.font.render('Inventory', True, (255, 255, 255))  # White text
		self.screen.blit(text_surface, (button_rect.x + 5, button_rect.y + 5))

	def draw_inventory(self):
		inventory_rect = pygame.Rect(self.width - 310, 50, 310, 130)  # Inventory window
		pygame.draw.rect(self.screen, (128, 128, 128), inventory_rect)  # Gray background

		# Draw slots
		slot_size = 50
		padding = 10
		for row in range(2):
			for col in range(5):
				slot_rect = pygame.Rect(inventory_rect.x + padding + (slot_size + padding) * col,
										inventory_rect.y + padding + (slot_size + padding) * row,
										slot_size, slot_size)
				pygame.draw.rect(self.screen, (255, 255, 255), slot_rect)  # White slot border

	def update_screen(self, player, inventory_visible, inventory_button):
		self.refresh_background()
		self.draw_player(player)
		self.draw_inventory_button(inventory_button)
		if inventory_visible:
			self.draw_inventory()
		self.clock.tick(self.clock_tick)
		pygame.display.update()