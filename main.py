"""
Names: Derek Wang, Suchit Basineni, Bhargav Yerramsetty
Date: 5/31/2024
main.py
Description: This file contains the main game loop and logic for the survival game.
"""


import sys
import random
import pygame
from player import HumanPlayer, Raft
from screen import Screen
from collidable import Collidable
import time
from OceanWaves import OceanWaves


# Define the cooldown period for resource collection in milliseconds
collection_cooldown = 2500
# Initialize the last collection time to a negative value to allow immediate collection
last_collection_time = -2500
# Initialize the last hunger decrease time, temperature change time, and wave collision time to the current time
last_hunger_decrease_time = time.time()
last_temperature_change_time = time.time()
last_wave_collision_time = time.time()

# Define a function to handle resource collection
def handle_resource_collection(screen, player, player_rect, current_time_ticks):
    # Declare the global variable for the last collection time
    global last_collection_time

    # Check if the cooldown period has passed since the last collection
    if current_time_ticks - last_collection_time >= collection_cooldown:
        # Initialize flags for each type of resource to False
        palm = False
        wood = False
        vine = False
        ore = False
        rock = False
        fish = False
        salt = False

        # Check each collidable object on the screen
        for collidable in screen.collidable_objects:
            # If the player is colliding with the object
            if collidable.rect.colliderect(player_rect):
                # Set the corresponding flag to True based on the object's layer
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
                elif 'Salt' in collidable.layer and player.has_item_in_inventory("torch"):
                    salt = True

        # Determine the type of item collected based on the flags
        if palm:
            item_collected = random.choice(['berry', 'leaf'])
        if wood:
            item_collected = 'wood'
        if vine:
            item_collected = 'vine'
        if ore:
            item_collected = random.choice(['rock', 'coal'])
        if rock:
            item_collected = 'rock'
        if fish:
            # If the player has a spear, they can collect fish
            if player.has_spear:
                item_collected = 'fish'
            else:
                # Otherwise, display a dialog box telling the player they need a spear
                screen.add_dialog_box("You need a spear (3 wood, 3 rock, 3 vine) to catch fish.", 2)
        if salt:
            item_collected = random.choice(['rock', 'coal', 'salt'])
        # If any resource was collected
        if palm or wood or vine or ore or rock or (fish and player.has_spear) or salt:
            # Update the last collection time to the current time
            last_collection_time = current_time_ticks
            # Determine a random quantity of the item to collect
            quantity_collected = random.randint(1, 3)
            # Add the collected item to the player's inventory
            player.add_item(item_collected, quantity_collected)
            # Display a dialog box showing what and how much was collected
            screen.add_dialog_box(f"Collected {quantity_collected} {item_collected}.", 2)


def play_game(screen, player):
    # Declare global variables for tracking time and speed
    global last_collection_time, last_hunger_decrease_time, last_temperature_change_time, last_wave_collision_time
    global speed
    speed = 6

    game_over = False
    current_background = "BEACH"
    inventory_open = False
    items = ["leaf", "wood", "fish", "rock", "coal", "salt", "berry", "vine"]
    
    # Add initial dialog boxes with instructions and storyline
    screen.add_dialog_box("I fell overboard while fishing. Now I'm stranded, and I need resources to survive and escape.", 15)
    screen.add_dialog_box("Press E to open/close inventory", 15)
    screen.add_dialog_box("Press F near objects to gather resources", 15)
    
    # Initialize waves if the background is set to OCEAN
    if current_background == "OCEAN":
        for _ in range(4):
            screen.waves.append(OceanWaves(screen.internal_width, screen.internal_height))

    # Main game loop
    while not game_over:
        player_rect = player.get_hitbox()
        current_time = time.time()
        current_time_ticks = pygame.time.get_ticks()
        
        # Handle various events such as quitting, resizing, key presses, and mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen.handle_resize(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    inventory_open = not inventory_open
                    if inventory_open and not player.inventory_opened:
                        screen.add_dialog_box("Left click items in inventory to remove.", 7)
                        player.inventory_opened = True
                elif event.key == pygame.K_c:
                    item = random.choice(items)
                    quantity = random.randint(1, 5)
                    player.add_item(item, quantity)
                if event.key == pygame.K_f:
                    handle_resource_collection(screen, player, player_rect, current_time_ticks)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if inventory_open:
                    for index, rect in enumerate(screen.inventory_positions):
                        if rect.collidepoint(mouse_pos):
                            player.clear_inventory_slot(index)
                for rect, text in screen.dialog_boxes:
                    if rect.collidepoint(mouse_pos):
                        screen.handle_crafting_click(player, text)

        # Handle player movement based on key presses
        keys = pygame.key.get_pressed()
        if not inventory_open:
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] and player.x > 0:
                dx -= 1
            if keys[pygame.K_RIGHT] and player.x < screen.internal_width - player.width:
                dx += 1
            if keys[pygame.K_UP] and player.y > 0:
                dy -= 1
            if keys[pygame.K_DOWN] and player.y < screen.internal_height - player.height:
                dy += 1

            # Normalize diagonal movement
            if dx != 0 and dy != 0:
                dx /= 1.41421356  # sqrt(2)
                dy /= 1.41421356  # sqrt(2)

            player.move(dx * speed, dy * speed)

            # Restrict player within the internal resolution
            player.x = max(0, min(player.x, screen.internal_width - player.width))
            player.y = max(0, min(player.y, screen.internal_height - player.height))

            # Handle collisions with objects
            handle_collisions(player, screen.collidable_objects)

            # Handle background transitions based on player's position and collected resources
            if current_background == "BEACH":
                if player.x <= 0 and keys[pygame.K_LEFT]:
                    screen.set_background("JUNGLE")
                    current_background = "JUNGLE"
                    player.x = screen.internal_width - player.width - 1
                elif player.x >= screen.internal_width - player.width and keys[pygame.K_RIGHT]:
                    if ((player.check_item_quantity("fish", 15) and 
                        player.check_item_quantity("salt", 15) and 
                        player.check_item_quantity("vine", 10) and 
                        player.check_item_quantity("wood", 10) and 
                        player.check_item_quantity("leaf", 10))):
                        screen.set_background("OCEAN")
                        current_background = "OCEAN"
                        player = Raft(1, player.y, player.max_health, player.health, player.max_hunger, player.hunger, player.max_temperature, player.temperature)  # Change player to raft
                        speed = 3
                        screen.entrance_dialog_added = False
                        screen.add_dialog_box("Escape by going right! Avoid the waves!", 7)
                        screen.waves = [OceanWaves(screen.internal_width, screen.internal_height) for _ in range(4)]  # Spawn waves when entering the ocean
                    elif not screen.entrance_dialog_added:
                        screen.add_dialog_box("You need resources for raft and food (15 fish, 15 salt, 10 vine, 10 wood, 10 leaf).", 7)
                        screen.entrance_dialog_added = True
                elif screen.entrance_dialog_added:
                        screen.dialog_messages = [msg for msg in screen.dialog_messages if msg[0] != "You need resources for raft and food (15 fish, 15 salt, 10 vine, 10 wood, 10 leaf)."]
                        screen.entrance_dialog_added = False

            elif current_background == "JUNGLE":
                if player.x <= 0 and keys[pygame.K_LEFT]:
                    screen.set_background("POND")
                    current_background = "POND"
                    player.x = screen.internal_width - player.width - 1
                elif player.y <= 0 and keys[pygame.K_UP]:
                    screen.set_background("MOUNTAIN")
                    current_background = "MOUNTAIN"
                    player.y = screen.internal_height - player.height - 1
                elif player.x >= screen.internal_width - player.width and keys[pygame.K_RIGHT]:
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

                if player.y >= screen.internal_height - player.height and keys[pygame.K_DOWN]:
                    screen.set_background("JUNGLE")
                    current_background = "JUNGLE"
                    player.y = 1
                elif entrance_collided:
                    if player.has_item_in_inventory("pulley"):
                        screen.set_background("CAVE")
                        current_background = "CAVE"
                        player.x = 115
                        player.y = 320
                        screen.entrance_dialog_added = False  # Reset the flag when transitioning
                        screen.add_dialog_box("You need a torch (2 wood, 3 vine, 4 leaf, 3 coal).", 7)
                    elif not screen.entrance_dialog_added:
                            screen.add_dialog_box("A rock is blocking the way. You need a pulley (4 wood 4 vine).")
                            screen.entrance_dialog_added = True
                elif screen.entrance_dialog_added:
                        screen.dialog_messages = [msg for msg in screen.dialog_messages if msg[0] != "A rock is blocking the way. You need a pulley to proceed."]
                        screen.entrance_dialog_added = False

            elif current_background == "CAVE":
                entrance_collided = False
                player_rect = player.get_hitbox()
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
                elif player.x >= screen.internal_width - player.width and keys[pygame.K_RIGHT]:
                    screen.set_background("JUNGLE")
                    current_background = "JUNGLE"
                    player.x = 1

            elif current_background == "OCEAN":

                # Move waves and check for collisions
                for oceanWaves in screen.waves:
                    oceanWaves.move()
                    if oceanWaves.get_hitbox().colliderect(player.get_hitbox()):
                        if current_time - last_wave_collision_time >= 1:
                            player.decrease_health(6)
                            last_wave_collision_time = current_time

                # Remove waves that have moved off-screen and spawn new ones
                screen.waves = [oceanWaves for oceanWaves in screen.waves if oceanWaves.x + oceanWaves.width > 0]
                while len(screen.waves) < 5:
                    screen.waves.append(OceanWaves(screen.internal_width, screen.internal_height))

                if player.x >= screen.internal_width - player.width:
                    screen.win_screen()
                    game_over = True

        # Decrease player's hunger over time
        if current_time - last_hunger_decrease_time >= 30:
            player.decrease_hunger()
            last_hunger_decrease_time = current_time

        # Adjust temperature based on the current background
        if current_background == "MOUNTAIN":
            if current_time - last_temperature_change_time >= 2:
                player.decrease_temperature()
                last_temperature_change_time = current_time

            if player.temperature <= 0 and current_time - player.last_health_decrease_time >= 1:
                player.decrease_health()
                player.last_health_decrease_time = current_time
        else:
            if current_time - last_temperature_change_time >= 5:
                player.increase_temperature()
                last_temperature_change_time = current_time

        # Decrease player's health if hunger reaches zero
        if player.hunger <= 0 and current_time - player.last_health_decrease_time >= 10:
            player.decrease_health()
            player.last_health_decrease_time = current_time

        # Check for player death
        if player.health <= 0:
            screen.death_screen()
            game_over = True

        # Update crafting prompts and screen display
        cooldown_ratio = min(1, (pygame.time.get_ticks() - last_collection_time) / collection_cooldown)
        can_craft_spear, can_craft_torch, can_craft_pulley = player.check_crafting_requirements()
        crafting_prompts = []
        if can_craft_spear:
            crafting_prompts.append("Click this box to craft a spear")
        if can_craft_torch:
            crafting_prompts.append("Click this box to craft a torch")
        if can_craft_pulley:
            crafting_prompts.append("Click this box to craft a pulley")

        screen.update_screen(player, inventory_open, cooldown_ratio, crafting_prompts)


def handle_collisions(player, collidables):
    # Get the player's hitbox
    player_rect = player.get_hitbox()
    
    # Iterate through all collidable objects
    for collidable in collidables:
        if 'Collidables' in collidable.layer:
            # Check if the player's hitbox collides with the collidable object
            if player_rect.colliderect(collidable):
                # Calculate diagonal speed for diagonal movements
                diagonal_speed = speed / 1.41421356
                # Adjust player's position based on the direction of movement
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
