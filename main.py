# Moonshot is a 2D space theme survival game. The player is tasked with using
# the ship's laser guns to destroy waves of enemies for as long as he can
# survive.
#
# Version 1.0
# Date: 12/1/2020
#
# Created by: Tyler Weir

# Local imports
from player import Player
from enemy import Enemy
from bullet import Bullet
from vector2d import Vector2D

# External imports
import pygame
import math
import json
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    K_RETURN,
    KEYDOWN,
    QUIT
)

# Initializes the pygame modules
pygame.init()

# Load in the background image
backgroundImage = pygame.image.load('sprites/background.png')

# Create the screen object
screen = pygame.display.set_mode((1920, 1080))
background = pygame.Surface(screen.get_size())
background.blit(backgroundImage, (0, 0))


# Makes groups of sprites that have built in methods such as collision
# detection
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

wave = 0

# Setup the clock to limit framerate
clock = pygame.time.Clock()


def best_score_rank(points):
    filename = 'scores.json'
    try:
        # Open the scores and add new entry
        with open(filename) as f:
            scores = json.load(f)
            scores.append(points)
            scores.sort(reverse=True)
    # Make file if there is no entry
    except FileNotFoundError:
        scores = [points]
        with open(filename, 'w') as f:
            json.dump(scores, f)
        return(score, 1)
    else:
        # Save the new entry
        with open(filename, 'w') as f:
            json.dump(scores, f)
        return(scores[0], scores.index(points)+1)


# Spawn enemies in corners
def spawn_enemies(wave):
    for i in range(wave):
        new_enemy = Enemy((0, 0))
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
        new_enemy = Enemy((1920, 0))
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
        new_enemy = Enemy((1920, 1080))
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
        new_enemy = Enemy((0, 1080))
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)


# Used to fire the lasers from the guns on the ship sprite
def fireLasers():
    x = player.rect.center[0]
    y = player.rect.center[1]

    # Get normal direction of player
    direction = Vector2D(-math.sin(player.get_direction()),
                         math.cos(player.get_direction()))
    direction.normalize()
    direction.scale(25)
    pos = direction.to_tuple()
    pos = (pos[0] + x, pos[1] + y)
    vel = (math.cos(player.get_direction()), math.sin(player.get_direction()))
    new_bullet = Bullet(vel, pos)
    bullets.add(new_bullet)
    all_sprites.add(new_bullet)

    # Add left bullet
    direction.scale(-1)
    pos = direction.to_tuple()
    pos = (pos[0] + x, pos[1] + y)
    new_bullet = Bullet(vel, pos)
    bullets.add(new_bullet)
    all_sprites.add(new_bullet)


# Define Fonts and words for menu
titleFont = pygame.font.SysFont('hack', 144)
title = titleFont.render('Moonshot', True, (173, 185, 204))
title_rect = title.get_rect(center=(1920/2, 1080/4))

actionFont = pygame.font.SysFont('hack', 72)
play = actionFont.render("Press 'enter' to play", True, (173, 185, 204))
play_rect = play.get_rect(center=(1920/2, 1080/2))

instructionsFont = pygame.font.SysFont('hack', 24)
instructions = instructionsFont.render("Spacebar: shoot   Arrowkeys: steer", True, (173, 185, 204))
instructions_rect = instructions.get_rect(center=(1920/2, 1080*3/5))

authorFont = pygame.font.SysFont('hack', 18)
author = authorFont.render("Created by: Tyler Weir  Version: 1.0", True, (173, 185, 204))
author_rect = author.get_rect(top=10, left=10)

# God Loop
running = True
while running:

    menu = True
    playing = True
    endScreen = True
    spawn_enemies(25)

    # Menu Loop
    while menu:
        # Loops through the event queue.
        for event in pygame.event.get():
            # Quit if the user clicks the quit button.
            if event.type == QUIT:
                running = False
                menu = False
                playing = False
                endScreen = False
            # Looks for a key pressed event.
            elif event.type == KEYDOWN:
                # Quit if the escape key is pressed.
                if event.key == K_ESCAPE:
                    running = False
                    menu = False
                    playing = False
                    endScreen = False
                # Start the game if enter is pressed
                if event.key == K_RETURN:
                    menu = False

        # Paint the background
        screen.blit(background, (0, 0))

        enemies.update(enemies, (-1, -1))  # Ignores the player

        for enemy in enemies:
            screen.blit(enemy.surf, enemy.rect)

        screen.blit(title, title_rect)
        screen.blit(play, play_rect)
        screen.blit(instructions, instructions_rect)
        screen.blit(author, author_rect)

        pygame.display.flip()

        # Ensure program maintains a rate of 60 frames per second
        clock.tick(60)

    for enemy in enemies:
        enemy.kill()

    # Instantiate the player
    player = Player()
    points = 0
    multiplier = 1
    all_sprites.add(player)

    scoreFont = pygame.font.SysFont('hack', 36)
    score = scoreFont.render("score: " + str(points), True, (173, 185, 204))
    score_rect = score.get_rect(right=1910, top=10)

    # Game loop!
    while playing:
        # Loops through the event queue.
        for event in pygame.event.get():
            # Quit if the user clicks the quit button.
            if event.type == QUIT:
                running = False
                playing = False
                endScreen = False
            # Looks for a key pressed event.
            elif event.type == KEYDOWN:
                # Quit if the escape key is pressed.
                if event.key == K_ESCAPE:
                    running = False
                    playing = False
                    endScreen = False
                # Fire a bullet from the player if space is pressed
                if event.key == K_SPACE:
                    fireLasers()

        if len(enemies) == 0:
            wave += 1
            spawn_enemies(wave)

        # Paint the background
        screen.blit(background, (0, 0))

        # Updates entities in these groups, providing necessary information
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update(enemies, player.rect.center)
        bullets.update()

        # Draws all sprites to the screen
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Kill the player if he collides with an enemy
        if pygame.sprite.spritecollideany(player, enemies):
            # Make a new player when the old one dies
            player.kill()
            playing = False
            wave = 0

        # Kill the enemy and the bullet if the bullet collides with an enemy
        for bullet in bullets:
            for enemy in enemies:
                if pygame.sprite.collide_rect(bullet, enemy):
                    bullet.kill()
                    enemy.kill()
                    points += multiplier
                    multiplier += 1
                    # Rerender the score text
                    score = scoreFont.render("Score: " + str(points), True, (173, 185, 204))
                    score_rect = score.get_rect(right=1910, top=10)

        screen.blit(score, score_rect)

        # Update the display to see new drawings
        pygame.display.flip()

        # Ensure program maintains a rate of 60 frames per second
        clock.tick(60)

    # Find the best score and the rank of current score and add to file
    scoreAndRank = best_score_rank(points)  # (bestScore, Rank)

    # Text used to show the death message
    deathFont = pygame.font.SysFont('hack', 144)
    death = deathFont.render('Game Over', True, (173, 185, 204))
    death_rect = death.get_rect(center=(1920/2, 1080/4))

    finalScoreFont = pygame.font.SysFont('hack', 72)
    finalScore = finalScoreFont.render(
        "Score: " + str(points) + "    Rank: " + str(scoreAndRank[1]), True, (173, 185, 204))
    finalScore_rect = finalScore.get_rect(center=(1920/2, 1080/2))

    bestScoreFont = pygame.font.SysFont('hack', 72)
    bestScore = bestScoreFont.render("Best: " + str(scoreAndRank[0]), True, (173, 185, 204))
    bestScore_rect = bestScore.get_rect(center=(1920/2, 1080*3/4))

    instructionsFont = pygame.font.SysFont('hack', 24)
    instructions = instructionsFont.render("Enter: play again   Esc: quit", True, (173, 185, 204))
    instructions_rect = instructions.get_rect(center=(1920/2, 1080/3))

    # Death Screen
    while endScreen:
        # Loops through the event queue.
        for event in pygame.event.get():
            # Quit if the user clicks the quit button.
            if event.type == QUIT:
                running = False
                endScreen = False
            # Looks for a key pressed event.
            elif event.type == KEYDOWN:
                # Quit if the escape key is pressed.
                if event.key == K_ESCAPE:
                    running = False
                    endScreen = False
                # Restart the game game if enter is pressed
                if event.key == K_RETURN:
                    endScreen = False

        # Paint the background
        screen.blit(background, (0, 0))

        bullets.update()
        enemies.update(enemies, (-1, -1))  # Ignores the player

        for sprite in all_sprites:
            screen.blit(sprite.surf, sprite.rect)

        screen.blit(death, death_rect)
        screen.blit(finalScore, finalScore_rect)
        screen.blit(bestScore, bestScore_rect)
        screen.blit(instructions, instructions_rect)

        pygame.display.flip()

        # Ensure program maintains a rate of 60 frames per second
        clock.tick(60)

    for enemy in enemies:
        enemy.kill()

# Quits the program when the game loop ends.
pygame.quit()
