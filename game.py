import random
from player import Enemy


class Game:
	Enemy = Enemy
	def __init__(self, speed=10, score=0, max_enemies=10, delay=0.1):
		self.speed = speed
		self.score = score
		self.max_enemies = max_enemies
		self.delay = delay
		self.enemy_list = []


	def drop_enemies(self, screen_width):
		delay = random.random()
		if len(self.enemy_list) < self.max_enemies and delay < self.delay:
			random_x = random.randint(0, screen_width)
			y_pos = 0
			enemy = self.Enemy(random_x, y_pos)
			self.enemy_list.append(enemy)


	

	def collision_check(self, player):
		for enemy in self.enemy_list:
			if enemy.detect_collision(player):
				return True
		return False
