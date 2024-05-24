import sys
import pygame
import random
from player import Enemy
sys.path.insert(0, '/rooms/')
#from river_room import River



class Game:
	Enemy = Enemy
	def __init__(self, speed=10, score=0, max_enemies=10, delay=0.1, setting=""):
		self.speed = speed
		self.score = score
		self.max_enemies = max_enemies
		self.delay = delay
		self.enemy_list = []
		self.setting = setting


	def drop_enemies(self, screen_width):
		delay = random.random()
		if len(self.enemy_list) < self.max_enemies and delay < self.delay:
			random_x = random.randint(0, screen_width)
			y_pos = 0
			enemy = self.Enemy(random_x, y_pos)
			self.enemy_list.append(enemy)

	def set_setting(self, newSetting):
		self.setting = newSetting
		# if self.setting == "BEACH":
		# 	beach = Beach()
		# if self.setting == "CAVE":
		# 	cave = Cave()
		# if self.setting == "JUNGLE":
		# 	jungle = Jungle()
		# if self.setting == "MOUNTAIN":
		# 	mountain = Mountain()
		# if self.setting == "OCEAN":
		# 	ocean = Ocean()
		# if self.setting == "RIVER":
		# 	river = River()
		
		

	

	def collision_check(self, player):
		for enemy in self.enemy_list:
			if enemy.detect_collision(player):
				return True
		return False
