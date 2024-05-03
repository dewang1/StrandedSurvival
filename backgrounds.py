from PIL import Image
import pygame


class Backgrounds:
	BEACH = pygame.image.load("backgrounds/beachBackground.jpg").convert()
	CAVE = pygame.image.load("backgrounds/caveBackground.jpg").convert()
	MOUNTAIN = pygame.image.load("backgrounds/mountainBackground.jpg").convert()
	OCEAN = pygame.image.load("backgrounds/oceanBackground.png").convert()
	RIVER = pygame.image.load("backgrounds/riverBackground.jpg").convert()