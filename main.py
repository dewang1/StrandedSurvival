import sys
import pygame
from player import HumanPlayer
from screen import Screen

speed = 6

def play_game(screen, player):
    game_over = False
    current_background = "BEACH"  # Starting background
    last_background = None  # To prevent immediate re-triggering of background transitions

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] and player.x > 0:
            dx -= 1
        if keys[pygame.K_RIGHT] and player.x < screen.width - player.size:
            dx += 1
        if keys[pygame.K_UP] and player.y > 0:
            dy -= 1
        if keys[pygame.K_DOWN] and player.y < screen.height - player.size:
            dy += 1

        if dx != 0 and dy != 0:
            dx /= 1.41421356  # sqrt(2)
            dy /= 1.41421356  # sqrt(2)

        player.move(dx * speed, dy * speed)

        # Background transitions based on the current environment and player's position
        if current_background == "BEACH":
            if player.x <= 0 and last_background != "JUNGLE":
                screen.set_background("JUNGLE")
                current_background = "JUNGLE"
                player.x = screen.width - player.size - 1
                last_background = "JUNGLE"
            elif player.x >= screen.width - player.size and last_background != "OCEAN":
                screen.set_background("OCEAN")
                current_background = "OCEAN"
                player.x = 1
                last_background = "OCEAN"

        elif current_background == "JUNGLE":
            if player.x <= 0 and last_background != "RIVER":
                screen.set_background("RIVER")
                current_background = "RIVER"
                player.x = screen.width - player.size - 1
                last_background = "RIVER"
            elif player.y <= 0 and last_background != "MOUNTAIN":
                screen.set_background("MOUNTAIN")
                current_background = "MOUNTAIN"
                player.y = screen.height - player.size - 1
                last_background = "MOUNTAIN"
            elif player.x >= screen.width - player.size and last_background != "BEACH":
                screen.set_background("BEACH")
                current_background = "BEACH"
                player.x = 1
                last_background = "BEACH"

        elif current_background == "MOUNTAIN":
            if player.y >= screen.height - player.size and last_background != "JUNGLE":
                screen.set_background("JUNGLE")
                current_background = "JUNGLE"
                player.y = 1
                last_background = "JUNGLE"
            elif player.x >= screen.width - player.size and last_background != "CAVE":
                screen.set_background("CAVE")
                current_background = "CAVE"
                player.x = 1
                last_background = "CAVE"

        elif current_background == "CAVE":
            if player.x <= 0 and last_background != "MOUNTAIN":
                screen.set_background("MOUNTAIN")
                current_background = "MOUNTAIN"
                player.x = screen.width - player.size - 1
                last_background = "MOUNTAIN"

        elif current_background == "RIVER":
            if player.x <= 0:
                player.x = 0  # Boundary, no transition to another area
            elif player.x >= screen.width - player.size and last_background != "JUNGLE":
                screen.set_background("JUNGLE")
                current_background = "JUNGLE"
                player.x = 1
                last_background = "JUNGLE"

        elif current_background == "OCEAN":
            if player.x <= 0 and last_background != "BEACH":
                screen.set_background("BEACH")
                current_background = "BEACH"
                player.x = screen.width - player.size - 1
                last_background = "BEACH"

        screen.update_screen(player)

if __name__ == "__main__":
    pygame.init()
    screen = Screen()  # Make sure display.set_mode() is correctly configured in the Screen class
    player = HumanPlayer(screen.width / 2, screen.height - 100)
    play_game(screen, player)
