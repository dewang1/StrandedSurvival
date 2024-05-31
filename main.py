import sys
import random
import pygame
from player import HumanPlayer
from screen import Screen
from collidable import Collidable
import random

speed = 6
collection_cooldown = 5000  # 5000 milliseconds = 5 seconds
last_collection_time = -5000

def play_game(screen, player):
    global last_collection_time  # Make sure to declare this as global to modify it within the function

    game_over = False
    current_background = "BEACH"  # Starting background
    inventory_open = False  # Track if the inventory is open
    items = ["leaf", "wood", "fish", "rock", "coal", "salt", "berry"]

    while not game_over:
        player_rect = pygame.Rect(player.x + 20, player.y + 40, player.size - 40, player.size - 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen.handle_resize(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    inventory_open = not inventory_open  # Toggle inventory state
                elif event.key == pygame.K_c:
                    item = random.choice(items)
                    quantity = random.randint(1, 5)
                    player.add_item(item, quantity)
                elif event.key == pygame.K_f:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_collection_time >= collection_cooldown:
                        palm = False
                        wood = False
                        vine = False
                        ore = False
                        rock = False
                        fish = False
                        salt = False

                        for collidable in screen.collidable_objects:
                            if collidable.rect.colliderect(player_rect):
                                if 'Palm' in collidable.layer:
                                    palm = True
                                elif 'Wood' in collidable.layer:
                                    wood = True
                                elif 'Vine' in collidable.layer:
                                    vine = True
                                elif 'Ore' in collidable.layer:
                                    ore = True
                                elif 'Rock' in collidable.layer:
                                    rock = True
                                elif 'Fish' in collidable.layer:
                                    fish = True
                                elif 'Salt' in collidable.layer:
                                    salt = True
                        if palm:
                            player.add_item(random.choice(['berry', 'leaf']), random.randint(1, 3))
                            print("Collected item from palm tree.")
                            last_collection_time = current_time
                        if wood:
                            player.add_item('wood', random.randint(1, 3))
                            print("Collected wood.")
                            last_collection_time = current_time
                        if vine:
                            player.add_item('vine', random.randint(1, 3))
                            print("Collected vine.")
                            last_collection_time = current_time
                        if ore:
                            player.add_item(random.choice(['rock', 'coal']), random.randint(1, 3))
                            print("Collected item from ore.")
                            last_collection_time = current_time
                        if rock:
                            player.add_item('rock', random.randint(1, 3))
                            print("Collected rock.")
                            last_collection_time = current_time
                        if fish:
                            player.add_item('fish', random.randint(1, 3))
                            print("Collected fish.")
                            last_collection_time = current_time
                        if salt:
                            player.add_item(random.choice(['rock', 'coal', 'salt']), random.randint(1, 3))
                            print("Collected salt.")
                            last_collection_time = current_time

        keys = pygame.key.get_pressed()
        if not inventory_open:  # Prevent movement when inventory is open
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] and player.x > 0:
                dx -= 1
            if keys[pygame.K_RIGHT] and player.x < screen.internal_width - player.size:
                dx += 1
            if keys[pygame.K_UP] and player.y > 0:
                dy -= 1
            if keys[pygame.K_DOWN] and player.y < screen.internal_height - player.size:
                dy += 1

            if dx != 0 and dy != 0:
                dx /= 1.41421356  # sqrt(2)
                dy /= 1.41421356  # sqrt(2)

            player.move(dx * speed, dy * speed)

            # Restrict player within the internal resolution
            player.x = max(0, min(player.x, screen.internal_width - player.size))
            player.y = max(0, min(player.y, screen.internal_height - player.size))

            # Handle collisions
            handle_collisions(player, screen.collidable_objects)

            # Background transitions based on the current environment and player's position
            if current_background == "BEACH":
                if player.x <= 0 and keys[pygame.K_LEFT]:
                    screen.set_background("JUNGLE")
                    current_background = "JUNGLE"
                    player.x = screen.internal_width - player.size - 1
                elif player.x >= screen.internal_width - player.size and keys[pygame.K_RIGHT]:
                    screen.set_background("OCEAN")
                    current_background = "OCEAN"
                    player.x = 1

            elif current_background == "JUNGLE":
                if player.x <= 0 and keys[pygame.K_LEFT]:
                    screen.set_background("POND")
                    current_background = "POND"
                    player.x = screen.internal_width - player.size - 1
                elif player.y <= 0 and keys[pygame.K_UP]:
                    screen.set_background("MOUNTAIN")
                    current_background = "MOUNTAIN"
                    player.y = screen.internal_height - player.size - 1
                elif player.x >= screen.internal_width - player.size and keys[pygame.K_RIGHT]:
                    screen.set_background("BEACH")
                    current_background = "BEACH"
                    player.x = 1

            elif current_background == "MOUNTAIN":
                # Check for collision with Entrance object layer
                entrance_collided = False
                for collidable in screen.collidable_objects:
                    if collidable.rect.colliderect(player_rect) and 'Entrance' in collidable.layer:
                        entrance_collided = True
                        break

                if player.y >= screen.internal_height - player.size and keys[pygame.K_DOWN]:
                    screen.set_background("JUNGLE")
                    current_background = "JUNGLE"
                    player.y = 1
                elif entrance_collided:
                    screen.set_background("CAVE")
                    current_background = "CAVE"
                    player.x = 115
                    player.y = 320

            elif current_background == "CAVE":
                entrance_collided = False
                player_rect = pygame.Rect(player.x + 20, player.y + 40, player.size - 40, player.size - 40)
                for collidable in screen.collidable_objects:
                    if collidable.rect.colliderect(player_rect) and 'Entrance' in collidable.layer:
                        entrance_collided = True
                        break
                if entrance_collided:
                    screen.set_background("MOUNTAIN")
                    current_background = "MOUNTAIN"
                    player.x = 694
                    player.y = 125

            elif current_background == "POND":
                if player.x <= 0:
                    player.x = 0  # Boundary, no transition to another area
                elif player.x >= screen.internal_width - player.size and keys[pygame.K_RIGHT]:
                    screen.set_background("JUNGLE")
                    current_background = "JUNGLE"
                    player.x = 1

            elif current_background == "OCEAN":
                if player.x <= 0 and keys[pygame.K_LEFT]:
                    screen.set_background("BEACH")
                    current_background = "BEACH"
                    player.x = screen.internal_width - player.size - 1

        # Calculate cooldown ratio
        current_time = pygame.time.get_ticks()
        cooldown_ratio = min(1, (current_time - last_collection_time) / collection_cooldown)

        screen.update_screen(player, inventory_open, cooldown_ratio)

def handle_collisions(player, collidables):
    player_rect = pygame.Rect(player.x + 20, player.y + 40, player.size - 40, player.size - 40)
    for collidable in collidables:
        if 'Collidables' in collidable.layer:
            if player_rect.colliderect(collidable):
                diagonal_speed = speed / 1.41421356
                if player.movement == 'up':
                    player.y += speed
                elif player.movement == 'down':
                    player.y -= speed
                elif player.movement == 'left':
                    player.x += speed
                elif player.movement == 'right':
                    player.x -= speed
                elif player.movement == 'up-right':
                    player.y += diagonal_speed
                    player.x -= diagonal_speed
                elif player.movement == 'up-left':
                    player.y += diagonal_speed
                    player.x += diagonal_speed
                elif player.movement == 'down-right':
                    player.y -= diagonal_speed
                    player.x -= diagonal_speed
                elif player.movement == 'down-left':
                    player.y -= diagonal_speed
                    player.x += diagonal_speed

if __name__ == "__main__":
    pygame.init()
    screen = Screen()  # Default starts with BEACH background
    player = HumanPlayer(screen.internal_width / 2, screen.internal_height - 100, 20, 20, 20, 20, 20, 20)
    play_game(screen, player)