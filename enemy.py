import pygame
import random
import math
import pilot

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
        self.velocity = (random.randint(-2, 2), random.randint(-2, 2))

        # Point in direction of inital velocity
        initial_angle = self.calc_rotation(self.velocity)
        self.surf = pygame.transform.rotate(enemySurf, initial_angle)
        self.rect = self.surf.get_rect(center=(random.randint(0, 800),
                                               random.randint(0, 800)))
        self.max_velocity = 3

    def update(self, enemies):
        # Move following the velocity vector
        self.rect.move_ip(self.velocity)
        # if self.rect.right < 0 or self.rect.left > 800 or self.rect.top > 820 or self.rect.top < -20:
        # self.kill()

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
        self.velocity = (self.velocity[0] + acceleration[0],
                         self.velocity[1] + acceleration[1])
        if(self.vector_magnitude(self.velocity) > self.max_velocity):
            self.velocity = self.scale_vector(
                self.normalize_vector(self.velocity), self.max_velocity)

        # Rotate to align with the new velocity
        # Maybe normalize first? I couldn't see much improvement
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

    def calc_rotation(self, v):
        newtheta = math.atan2(v[1], v[0])
        return 180-math.degrees(newtheta)

    def normalize_vector(self, vector):
        magnitude = self.vector_magnitude(vector)

        if magnitude == 0:
            return vector
        else:
            return(vector[0]/magnitude, vector[1]/magnitude)

    def scale_vector(self, vector, scale):
        return (vector[0]*scale, vector[1]*scale)

    def vector_magnitude(self, vector):
        return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
