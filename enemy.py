import pygame
import random
import pilot
from vector2d import Vector2D

#   Load the sprite images for the enemies
enemyImages = [pygame.image.load('sprites/enemy_1.png'),
               pygame.image.load('sprites/enemy_2.png'),
               pygame.image.load('sprites/enemy_3.png'),
               pygame.image.load('sprites/enemy_4.png')]


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # initialize the super sprite class
        super(Enemy, self).__init__()

        self.frames = 0

        # Make a pilot for acceleration control
        self.pilot = pilot.Pilot()
        # Setup the movement vectors
        self.velocity = Vector2D(random.randint(-2, 2), random.randint(-2, 2))

        self.surf = self.makeSurface()
        self.rect = self.surf.get_rect(center=(random.randint(0, 800),
                                               random.randint(0, 800)))
        self.max_velocity = 3

    def update(self, enemies, playerPos):
        # Move following the velocity vector
        self.rect.move_ip(self.velocity.to_tuple())

        # Loop Screen
        if(self.rect.right < 0):
            self.rect.left = 1920
        if(self.rect.left > 1920):
            self.rect.right = 0
        if(self.rect.top > 1080):
            self.rect.bottom = 0
        if(self.rect.bottom < 0):
            self.rect.top = 1080

        # Get accerlation from the pilot.
        acceleration = self.pilot.get_acceleration(self.rect.center,
                                                   self.velocity,
                                                   enemies,
                                                   playerPos)

        # Apply steering accerlation to velocity
        self.velocity.add(acceleration)

        # Scale back the velocity to normal speed
        self.velocity.normalize()
        self.velocity.scale(self.max_velocity)

        # Rotate to align with the new velocity
        # Maybe normalize first? I couldn't see much improvement
        theta = self.velocity.calc_angle()
        self.rotate(theta)

        # Update the counter for the images
        self.frames += 1
        if ((self.frames//8) > 3):
            self.frames = 0

    def rotate(self, angle):
        # save the old center postion
        oldCenter = self.rect.center

        # sets the current surface to the enemy surface rotated to the
        # indicated angle
        self.surf = pygame.transform.rotate(self.makeSurface(), angle+90)

        # get the rect of the rotated surf and set it's center to the saved
        self.rect = self.surf.get_rect()
        self.rect.center = oldCenter

    def makeSurface(self):
        # Create a surface that will represent the enemy
        enemySurf = pygame.Surface((10, 30))

        # blit the image onto the Surface
        enemySurf.set_colorkey((255, 0, 255))
        enemySurf.blit(enemyImages[self.frames//8], (0, 0))

        return enemySurf
