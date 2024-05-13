import sys
import pygame
from player import HumanPlayer
from screen import Screen
from game import Game

speed = 10
def play_game(screen, player, game):
    game_over = False
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] and player.x > 0:
            dx -= 1
        if keys[pygame.K_RIGHT] and player.x < (screen.width - player.size):
            dx += 1
        if keys[pygame.K_UP] and player.y > 0:
            dy -= 1
        if keys[pygame.K_DOWN] and player.y < (screen.height - player.size):
            dy += 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx /= 1.41421356  # sqrt(2)
            dy /= 1.41421356  # sqrt(2)

        player.x += dx*speed
        player.y += dy*speed

        #game.drop_enemies(screen.width)
        #game.update_enemy_positions(screen.height)
        game.set_level()

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


