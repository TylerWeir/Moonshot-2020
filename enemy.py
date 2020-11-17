import pygame
import random
import pilot
from vector2d import Vector2D

# Create a surface that will represent the enemy
enemySurf = pygame.Surface((10, 5))
enemySurf.fill((255, 255, 255))

# set a color key for blitting
enemySurf.set_colorkey((255, 0, 0))

# create shapes so you can tell rotation is happenning
smaller = pygame.Rect(0, 0, 5, 5)

# draw those two shapes to that surface
pygame.draw.rect(enemySurf, (255, 75, 75), smaller)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # initialize the super sprite class
        super(Enemy, self).__init__()

        # Make a pilot for acceleration control
        self.pilot = pilot.Pilot()
        # Setup the movement vectors
        self.velocity = Vector2D(random.randint(-2, 2), random.randint(-2, 2))

        # Point in direction of inital velocity
        initial_angle = self.velocity.calc_angle()
        self.surf = pygame.transform.rotate(enemySurf, initial_angle)
        self.rect = self.surf.get_rect(center=(random.randint(0, 800),
                                               random.randint(0, 800)))
        self.max_velocity = 3

    def update(self, enemies):
        # Move following the velocity vector
        self.rect.move_ip(self.velocity.to_tuple())

        # Loop screen
        if(self.rect.right < 0):
            self.rect.left = 800
        if(self.rect.left > 800):
            self.rect.right = 0
        if(self.rect.top > 800):
            self.rect.bottom = 0
        if(self.rect.bottom < 0):
            self.rect.top = 800

        # Get accerlation from the pilot.
        acceleration = self.pilot.get_acceleration(self.rect.center, enemies)

        # Apply acceleration to velocity
        self.velocity.add(acceleration)
        if(self.velocity.get_magnitude() > self.max_velocity):
            self.velocity.normalize_vector()
            self.velocity.scale(self.max_velocity)

        # Rotate to align with the new velocity
        # Maybe normalize first? I couldn't see much improvement
        theta = self.velocity.calc_angle()
        self.rotate(theta)

    def rotate(self, angle):
        # save the old center postion
        oldCenter = self.rect.center

        # sets the current surface to the enemy surface rotated to the
        # indicated angle
        self.surf = pygame.transform.rotate(enemySurf, angle)

        # get the rect of the rotated surf and set it's center to the saved
        self.rect = self.surf.get_rect()
        self.rect.center = oldCenter
