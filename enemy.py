import pygame
import random

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
        self.surf = enemySurf
        self.rect = self.surf.get_rect(center=(random.randint(820, 900),
                                               random.randint(0, 600)))
        self.speed = random.randint(1, 5)
        self.angle = 0

    def update(self):
        # move to the left at characteristic speed
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        self.rotate()

    def rotate(self):
        # Stores the position to give to the rotated rect
        oldCenter = self.rect.center

        # Keeps track of angle of rotation
        if self.angle < 360:
            self.angle += 1
        else:
            self.angle = 0

        # sets the current surface to the enemy surface rotated to the
        # indicated angle
        self.surf = pygame.transform.rotate(enemySurf, self.angle)

        # get the rect of the rotated surf and set it's center to the saved
        # old center
        self.rect = self.surf.get_rect()
        self.rect.center = oldCenter
