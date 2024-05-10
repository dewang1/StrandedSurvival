from backgrounds import Backgrounds
from color import Color
import pygame


class Screen:
	def __init__(self, width=800, height=640, font_type="monospace", font_size=35, clock_tick=60):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		self.bg_image = bg_image
		self.font = pygame.font.SysFont(font_type, font_size)
		self.clock = pygame.time.Clock()
		self.clock_tick = clock_tick
		self.bg_image='backgrounds/riverBackground.jpg'
	
	def refresh_background(self):
		image = pygame.image.load(self.bg_image).convert_alpha()
		background = pygame.transform.scale(image, (self.width, self.height))
		self.screen.blit(background, (0, 0))

	def draw_enemies(self, enemy_list):
		for enemy in enemy_list:
			enemy.draw(self.screen)

	def draw_player(self, player):
		player.draw(self.screen)

	def draw_score_label(self, score, color=Color.YELLOW):
		text = f"Score: {score}"
		label = self.font.render(text, 1, color)
		self.screen.blit(label, (self.width-200, self.height-40))

	def update_screen(self, enemy_list, player, score):
		self.refresh_background()
		self.draw_enemies(enemy_list)
		self.draw_player(player)

		self.clock.tick(self.clock_tick)
		pygame.display.update()