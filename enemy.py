import pygame
import random
import math
import pilot

# Create a surface that will represent the enemy
enemySurf = pygame.Surface((20, 10))
enemySurf.fill((255, 255, 255))

# set a color key for blitting
enemySurf.set_colorkey((255, 0, 0))

# create shapes so you can tell rotation is happenning
smaller = pygame.Rect(0, 0, 5, 10)

# draw those two shapes to that surface
pygame.draw.rect(enemySurf, (255, 75, 75), smaller)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # initialize the super sprite class
        super(Enemy, self).__init__()

        # Make a pilot for acceleration control
        self.pilot = pilot.Pilot()
        # Setup the movement vectors
        self.velocity = (random.randint(-2, 2), random.randint(-2, 2))

        # Point in direction of inital velocity
        initial_angle = self.calc_rotation(self.velocity)
        self.surf = pygame.transform.rotate(enemySurf, initial_angle)
        self.rect = self.surf.get_rect(center=(random.randint(0, 800),
                                               random.randint(0, 800)))

    def update(self, enemies):
        # Move following the velocity vector
        self.rect.move_ip(self.velocity)
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.top > 820 or self.rect.top < -20:
            self.kill()

        # Get accerlation from the pilot.
        acceleration = self.pilot.get_acceleration(self.rect.center, enemies)

        # Apply acceleration to velocity
        self.velocity = (self.velocity[0] + acceleration[0],
                         self.velocity[1] + acceleration[1])

        # Rotate to align with the new velocity
        if(acceleration[0] != 0 or acceleration[1] != 0):
            theta = self.calc_rotation(self.velocity)
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

    def calc_rotation(self, v2):
        newtheta = math.atan2(v2[1], v2[0])
        return 180-math.degrees(newtheta)
