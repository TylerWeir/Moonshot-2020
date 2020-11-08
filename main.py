"""This program is my submission to the 2020 Game Off hosted by itch.io"""
from player import Player
from enemy import Enemy

# Imports the pygame module
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)


# Initializes the pygame modules
pygame.init()

# Create the screen object
# Make the screen fullscreen mode
screen = pygame.display.set_mode((800, 800))

# instantitate our player; reight now he's just a rectangle
player = Player()

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# Makes groups of sprites that have built in methods such as collision
# detection
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Add a new eney every 250 miliseconds
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 100)

# Setup the clock to limit framerate
clock = pygame.time.Clock()

# Variable to keep the game running.
running = True

# Game loop!
while running:

    # Loops through the event queue.
    for event in pygame.event.get():
        # Quit if the user clicks the quit button.
        if event.type == QUIT:
            running = False
        # Looks for a key pressed event.
        elif event.type == KEYDOWN:
            # Quit if the escape key is pressed.
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.blit(background, (0, 0))

    # Moves the player when keys are pressed
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()

    # Draws all sprites to the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Kill the player if he collides with an enemy
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

    # Update the display to see new drawings
    pygame.display.flip()
    # print("Screen flipped")

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)

# Done! Time to quit.
pygame.quit()
