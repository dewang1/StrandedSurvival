from backgrounds import Backgrounds
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


	def update_screen(self, player):
		self.refresh_background()
		self.draw_player(player)

		self.clock.tick(self.clock_tick)
		pygame.display.update()