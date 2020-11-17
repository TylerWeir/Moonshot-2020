from vector2d import Vector2D
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
        self.velocity = Vector2D(0, 0)

    def update(self, pressed_keys):
        # Move following the velocity vector
        self.rect.move_ip(self.velocity.to_tuple())

        # Apply acceleration to velocity
        a = 0.1
        if pressed_keys[K_UP]:
            self.velocity.add(Vector2D(0, -a))
        if pressed_keys[K_DOWN]:
            self.velocity.add(Vector2D(0, a))
        if pressed_keys[K_LEFT]:
            self.velocity.add(Vector2D(-a, 0))
        if pressed_keys[K_RIGHT]:
            self.velocity.add(Vector2D(a, 0))

        # Damping the velocity
        self.velocity.scale(0.99)

        theta = self.velocity.calc_angle()
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
