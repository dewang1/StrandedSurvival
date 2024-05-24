import sys
import pygame
from player import HumanPlayer
from screen import Screen
from game import Game

speed = 10
def play_game(screen, player, game):
    game_over = False
    current_background = "BEACH"  # Starting background
    game.set_setting("BEACH")     # Setting specific game methods
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] and player.x > 0:
            player.sprite = player.walking_animation()
            dx -= 1

        if keys[pygame.K_RIGHT] and player.x < screen.width - player.size:
            player.sprite = player.walking_animation()
            dx += 1
        if keys[pygame.K_UP] and player.y > 0:
            player.sprite = player.walking_animation()
            dy -= 1
        if keys[pygame.K_DOWN] and player.y < screen.height - player.size:
            player.sprite = player.walking_animation()
            dy += 1

        if dx != 0 and dy != 0:
            dx /= 1.41421356  # sqrt(2)
            dy /= 1.41421356  # sqrt(2)

        player.x += dx * speed
        player.y += dy * speed

        # Background transitions based on the current environment and player's position
        if current_background == "BEACH":
            if player.x <= 0:
                screen.set_background("JUNGLE")
                current_background = "JUNGLE"
                game.set_setting("JUNGLE")
                player.x = screen.width - player.size
            elif player.x >= screen.width - player.size:
                screen.set_background("OCEAN")
                current_background = "OCEAN"
                game.set_setting("OCEAN")
                player.x = 0

        elif current_background == "JUNGLE":
            if player.x <= 0:
                screen.set_background("RIVER")
                current_background = "RIVER"
                game.set_setting("RIVER")
                player.x = screen.width - player.size
            elif player.y <= 0:
                screen.set_background("MOUNTAIN")
                current_background = "MOUNTAIN"
                game.set_setting("MOUNTAIN")
                player.y = screen.height - player.size
            elif player.x >= screen.width - player.size:
                screen.set_background("BEACH")
                current_background = "BEACH"
                game.set_setting("BEACH")
                player.x = 0

        elif current_background == "MOUNTAIN":
            if player.y >= screen.height - player.size:
                screen.set_background("JUNGLE")
                current_background = "JUNGLE"
                game.set_setting("JUNGLE")
                player.y = 0
            elif player.x >= screen.width - player.size:
                screen.set_background("CAVE")
                current_background = "CAVE"
                game.set_setting("CAVE")
                player.x = 0

        elif current_background == "CAVE":
            if player.x <= 0:
                screen.set_background("MOUNTAIN")
                current_background = "MOUNTAIN"
                game.set_setting("MOUNTAIN")
                player.x = screen.width - player.size

        elif current_background == "RIVER":
            if player.x <= 0:
                screen.set_background("JUNGLE")
                current_background = "JUNGLE"
                game.set_setting("JUNGLE")
                player.x = screen.width - player.size
            elif player.x >= screen.width - player.size:
                screen.set_background("OCEAN")
                current_background = "OCEAN"
                game.set_setting("OCEAN")
                player.x = 0

        elif current_background == "OCEAN":
            if player.x <= 0:
                screen.set_background("BEACH")
                current_background = "BEACH"
                game.set_setting("BEACH")
                player.x = screen.width - player.size

        
        screen.update_screen(game.enemy_list, player, game.score)

        if game.collision_check(player):
            game_over = True
            break



if __name__ == "__main__":
	pygame.init()
	screen = Screen()  # Now, this should occur after display.set_mode() is established.
	player = HumanPlayer(screen.width / 2, screen.height - 100)
	game = Game()
	play_game(screen, player, game)


