import pygame
from color import Color

class Player:
	def __init__(self, x, y, size, color):
		self.x = x
		self.y = y
		self.size = size
		self.color = color

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

	def detect_collision(self, other):
		if (other.x >= self.x and other.x < (self.x + self.size)) or (self.x >= other.x and self.x < (other.x + other.size)):
			if (other.y >= self.y and other.y < (self.y + self.size)) or (self.y >= other.y and self.y < (other.y + self.size)):
				return True
		return False

class Enemy(Player):
	def __init__(self, x, y):
		super().__init__(x, y, size=50, color=Color.BLUE)

class HumanPlayer(Player):
	def __init__(self, x, y):
		super().__init__(x, y, size=50, color=Color.RED)