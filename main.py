# Moonshot is a 2D space age dogfighting game. The player is tasked with
# defending his moon base for as long as he can survive. The enemy ships come
# in waves. Each wave contains squadrons of enemies that swoop upon the player
# and attempt to destroy him with projectiles.
#
# Created by: Tyler Weir
# Date: 11/9/2020
#
# TODO: Make vector class, add proper ordering of acceleration to pilot class
#

# Local imports
from player import Player
from enemy import Enemy
from bullet import Bullet
from vector2d import Vector2D

# External imports
import pygame
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT
)

# Initializes the pygame modules
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((1920, 1080))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# Instantiate the player
player = Player()

# Makes groups of sprites that have built in methods such as collision
# detection
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Add a new eney every 250 miliseconds with custom event detection and timer
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 200)

# Setup the clock to limit framerate
clock = pygame.time.Clock()

# Variable to keep the game running.
running = True


# Used to fire the lasers from the guns on the ship sprite
def fireLasers():
    x = player.rect.center[0]
    y = player.rect.center[1]

    # Get normal velocity of player
    direction = Vector2D(-player.velocity.y, player.velocity.x)
    direction.normalize()
    direction.scale(25)
    pos = direction.to_tuple()
    pos = (pos[0] + x, pos[1] + y)
    new_bullet = Bullet(player.velocity.to_tuple(), pos)
    bullets.add(new_bullet)
    all_sprites.add(new_bullet)

    # Add left bullet
    direction.scale(-1)
    pos = direction.to_tuple()
    pos = (pos[0] + x, pos[1] + y)
    new_bullet = Bullet(player.velocity.to_tuple(), pos)
    bullets.add(new_bullet)
    all_sprites.add(new_bullet)


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
            # Fire a bullet from the player if space is pressed
            if event.key == K_SPACE:
                fireLasers()
        # Custom event detection to add enemy
        elif event.type == ADDENEMY and len(enemies) < 10:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Paint the background
    screen.blit(background, (0, 0))

    # Updates entities in these groups, providing necessary information
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update(enemies, player)
    bullets.update()

    # Draws all sprites to the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Kill the player if he collides with an enemy
    if pygame.sprite.spritecollideany(player, enemies):
        # Make a new player when the old one dies
        player.kill()
        player = Player()
        all_sprites.add(player)

    # Kill the enemy and the bullet if the bullet collides with an enemy
    for bullet in bullets:
        for enemy in enemies:
            if pygame.sprite.collide_rect(bullet, enemy):
                bullet.kill()
                enemy.kill()

    # Update the display to see new drawings
    pygame.display.flip()

    # Ensure program maintains a rate of 60 frames per second
    clock.tick(60)

# Quits the program when the game loop ends.
pygame.quit()
