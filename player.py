import math
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

# Create a surface that will represent the player
playerSurf = pygame.Surface((20, 10))
playerSurf.fill((255, 255, 255))

# set a color key for blitting
playerSurf.set_colorkey((255, 0, 0))

# create shapes so you can tell rotation is happenning
smaller = pygame.Rect(0, 0, 5, 10)

# draw those two shapes to that surface
pygame.draw.rect(playerSurf, (75, 255, 75), smaller)


# Define our player object and call super to give it all the properties and
# methods of pygame.sprite.Sprite
# The surface we draw on the screen is now a propery of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = playerSurf
        self.rect = self.surf.get_rect()
        self.velocity = (0, 0)

    def update(self, pressed_keys):
        # Move following the velocity vector
        self.rect.move_ip(self.velocity)

        # Apply acceleration to velocity
        a = 0.1
        if pressed_keys[K_UP]:
            self.velocity = (self.velocity[0], self.velocity[1]-a)
        if pressed_keys[K_DOWN]:
            self.velocity = (self.velocity[0], self.velocity[1]+a)
        if pressed_keys[K_LEFT]:
            self.velocity = (self.velocity[0]-a, self.velocity[1])
        if pressed_keys[K_RIGHT]:
            self.velocity = (self.velocity[0]+a, self.velocity[1])

        # Damping the velocity
        self.velocity = (self.velocity[0]*0.99, self.velocity[1]*0.99)

        theta = self.calc_rotation(self.velocity)
        self.rotate(theta)

        # Loop the screen
        if self.rect.right < 0:
            self.rect.left = 800
        elif self.rect.left > 800:
            self.rect.right = 0
        if self.rect.top > 800:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = 800

    def rotate(self, angle):
        # save the old center postion
        oldCenter = self.rect.center

        # sets the current surface to the enemy surface rotated to the
        # indicated angle
        self.surf = pygame.transform.rotate(playerSurf, angle)

        # get the rect of the rotated surf and set it's center to the saved
        self.rect = self.surf.get_rect()
        self.rect.center = oldCenter

    def calc_rotation(self, v):
        newtheta = math.atan2(v[1], v[0])
        return 180-math.degrees(newtheta)
