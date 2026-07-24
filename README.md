# 2025_Game_5
Repo for group 5's choose your own adventure game: Stranded Survival: Island Escape
# Stranded Survival: Island Escape

A 2D survival adventure game where you must gather resources, craft tools, manage survival stats, and escape a mysterious island. Built with Python and Pygame.

## Overview

After falling overboard while fishing, you wake up stranded on an island with nothing but your wits. Survive by gathering resources, crafting essential tools, managing hunger and temperature, and navigating hazardous ocean waves. Your goal: reach the escape point on the right side of the island.

## Features

**Resource Gathering**
- Collect from 7 resource types: wood, rock, vine, berries, leaves, coal, fish, and salt
- Each resource type spawns 1-3 items per collection
- Some resources require tools (e.g., need a **spear** to fish, **torch** to harvest salt)

**Crafting System**
- **Spear** (3 wood + 3 rock + 3 vine) — Required to catch fish for food
- **Torch** (2 wood + 3 vine + 4 leaf + 3 coal) — Required to see and harvest in dark areas
- **Pulley** (4 wood + 5 vine) — Unlocks cave environment

**Survival Mechanics**
- **Hunger** — Decreases over time; must eat food (berries or fish) to survive
- **Health** — Damaged by ocean waves and starvation; defeat = game over
- **Temperature** — Changes dynamically; affects player comfort and resource availability

**Dynamic World**
- Procedurally spawning ocean waves with collision detection
- Inventory management
- Animated sprite system with directional movement
- Dialog system for tutorials and feedback

**Tile-based Map**
- Designed with Tiled map editor
- Multiple terrain types (beach, forest, ocean)
- Collision detection for terrain and obstacles

## Installation

### Requirements
- Python 3.x
- pygame
- pytmx
- pillow

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd StrandedSurvival-main

# Install dependencies
pip install pygame pytmx pillow

# Run the game
python main.py
```

## How to Play

**Controls**
- **Arrow Keys** or **WASD** — Move your character
- **I** — Open/close inventory
- **Mouse Click** — Select items, interact with UI, craft items
- **Space** — Interact with nearby objects/NPCs (if applicable)

**Gameplay Loop**

1. **Gather Resources**
2. **Craft Tools** 
3. **Manage Survival Stats**
4. **Create Boat**
5. **Sail Boat And Avoid Waves**
6. **Escape**

## Technical Details

**Features**
- **Sprite-based rendering** — Character has 4-directional animation (idle + walk frames)
- **Collision detection** — For player-resource and player-obstacle interactions
- **State management** — Tracks inventory, crafting availability, survival stats, and game progression
